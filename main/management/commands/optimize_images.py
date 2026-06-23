"""
One-shot optimizer for everything that was added before WebP conversion existed.

    python manage.py optimize_images              # static + media + templates + lazy
    python manage.py optimize_images --static     # only static/ images + template rewrite
    python manage.py optimize_images --media       # only already-uploaded media + DB
    python manage.py optimize_images --no-lazy     # skip adding loading="lazy"
    python manage.py optimize_images --dry-run     # report only, change nothing

New dashboard uploads convert themselves (see main/models.py save()), so this is
mainly to fix the heavy files already committed to the repo / database.
"""

import os
import re

from django.apps import apps
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from main.image_utils import CONVERTIBLE_EXTS, encode_webp_bytes, webp_name


# Models -> the ImageField names that should be migrated to .webp.
MEDIA_FIELDS = {
    "GalleryImage": ["image"],
    "CelebrationImage": ["image"],
    "ServiceSection": ["image_left", "image_right"],
    "MainService": ["card_image", "left_image", "right_image"],
    "CorporateEvent": ["main_image", "side_image"],
    "OtherService": ["image"],
}


class Command(BaseCommand):
    help = "Convert existing static + uploaded images to compressed WebP and update references."

    def add_arguments(self, parser):
        parser.add_argument("--static", action="store_true", help="Only process static images.")
        parser.add_argument("--media", action="store_true", help="Only process uploaded media.")
        parser.add_argument("--no-lazy", action="store_true", help="Do not add loading=lazy to <img>.")
        parser.add_argument("--no-templates", action="store_true", help="Do not rewrite template refs.")
        parser.add_argument("--dry-run", action="store_true", help="Report only; write nothing.")

    def handle(self, *args, **opts):
        do_static = opts["static"] or not opts["media"]
        do_media = opts["media"] or not opts["static"]
        self.dry = opts["dry_run"]

        self.saved_before = 0
        self.saved_after = 0

        if do_static:
            converted = self.convert_static()
            if not opts["no_templates"]:
                self.rewrite_templates(converted)
        if do_media:
            self.convert_media()
        if not opts["no_lazy"]:
            self.add_lazy_loading()

        delta = self.saved_before - self.saved_after
        self.stdout.write(self.style.MIGRATE_HEADING("\n==== SUMMARY ===="))
        self.stdout.write(
            f"Original size: {self.saved_before/1048576:.1f} MB  ->  "
            f"WebP size: {self.saved_after/1048576:.1f} MB  "
            f"(saved {delta/1048576:.1f} MB)"
        )
        if self.dry:
            self.stdout.write(self.style.WARNING("DRY RUN — nothing was written."))

    # ---------------------------------------------------------------- static
    def convert_static(self):
        """Convert main/static/main/images/** to .webp siblings. Returns {old_rel: new_rel}."""
        base = os.path.join(settings.BASE_DIR, "main", "static")
        images_root = os.path.join(base, "main", "images")
        mapping = {}
        if not os.path.isdir(images_root):
            self.stdout.write(self.style.WARNING(f"No static images dir at {images_root}"))
            return mapping

        self.stdout.write(self.style.MIGRATE_HEADING("\n== Static images =="))
        for dirpath, _dirs, files in os.walk(images_root):
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                if ext not in CONVERTIBLE_EXTS:
                    continue
                src = os.path.join(dirpath, fname)
                dst = os.path.splitext(src)[0] + ".webp"

                # Reference path as used inside templates, e.g. main/images/Foo.jpg
                rel_old = os.path.relpath(src, base).replace(os.sep, "/")
                rel_new = os.path.relpath(dst, base).replace(os.sep, "/")
                mapping[rel_old] = rel_new

                if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                    continue  # already up to date

                try:
                    data = encode_webp_bytes(src)
                except Exception as exc:
                    self.stdout.write(self.style.ERROR(f"  FAIL {rel_old}: {exc}"))
                    mapping.pop(rel_old, None)
                    continue

                before = os.path.getsize(src)
                self.saved_before += before
                self.saved_after += len(data)
                if not self.dry:
                    with open(dst, "wb") as fh:
                        fh.write(data)
                self.stdout.write(
                    f"  {rel_old}  {before/1024:.0f}KB -> {len(data)/1024:.0f}KB"
                )
        return mapping

    def rewrite_templates(self, mapping):
        """Replace every `main/images/X.ext` reference with its `.webp` sibling."""
        if not mapping:
            return
        templates_root = os.path.join(settings.BASE_DIR, "main", "templates")
        self.stdout.write(self.style.MIGRATE_HEADING("\n== Rewriting template references =="))
        # Longest paths first so 'images/a.png' doesn't partially clobber others.
        items = sorted(mapping.items(), key=lambda kv: -len(kv[0]))
        for dirpath, _dirs, files in os.walk(templates_root):
            for fname in files:
                if not fname.endswith(".html"):
                    continue
                path = os.path.join(dirpath, fname)
                with open(path, "r", encoding="utf-8") as fh:
                    text = fh.read()
                new_text = text
                hits = 0
                for old_rel, new_rel in items:
                    if old_rel in new_text:
                        hits += new_text.count(old_rel)
                        new_text = new_text.replace(old_rel, new_rel)
                if new_text != text:
                    if not self.dry:
                        with open(path, "w", encoding="utf-8") as fh:
                            fh.write(new_text)
                    rel = os.path.relpath(path, templates_root).replace(os.sep, "/")
                    self.stdout.write(f"  {rel}: {hits} reference(s) updated")

    # ---------------------------------------------------------------- media
    def convert_media(self):
        self.stdout.write(self.style.MIGRATE_HEADING("\n== Uploaded media (DB) =="))
        for model_name, fields in MEDIA_FIELDS.items():
            try:
                Model = apps.get_model("main", model_name)
            except LookupError:
                continue
            for obj in Model.objects.all():
                changed = False
                for field_name in fields:
                    field = getattr(obj, field_name, None)
                    if not field or not field.name:
                        continue
                    if field.name.lower().endswith(".webp"):
                        continue
                    storage = field.storage
                    old_name = field.name
                    if not storage.exists(old_name):
                        self.stdout.write(self.style.WARNING(f"  missing file: {old_name}"))
                        continue
                    try:
                        with storage.open(old_name, "rb") as fh:
                            data = encode_webp_bytes(fh)
                    except Exception as exc:
                        self.stdout.write(self.style.ERROR(f"  FAIL {old_name}: {exc}"))
                        continue

                    before = storage.size(old_name)
                    self.saved_before += before
                    self.saved_after += len(data)
                    new_basename = os.path.basename(webp_name(old_name))

                    if not self.dry:
                        field.save(new_basename, ContentFile(data), save=False)
                        try:
                            storage.delete(old_name)
                        except Exception:
                            pass
                    changed = True
                    self.stdout.write(
                        f"  {model_name}#{obj.pk} {field_name}: "
                        f"{before/1024:.0f}KB -> {len(data)/1024:.0f}KB"
                    )
                if changed and not self.dry:
                    # field.name is now '.webp', so the model's save() override
                    # detects nothing to convert and just persists the new path.
                    obj.save()

    # ---------------------------------------------------------------- lazy
    def add_lazy_loading(self):
        """Add loading="lazy" decoding="async" to <img> tags that lack them."""
        templates_root = os.path.join(settings.BASE_DIR, "main", "templates")
        self.stdout.write(self.style.MIGRATE_HEADING("\n== Lazy-loading <img> tags =="))
        # <img ...>  that doesn't already contain loading=
        pattern = re.compile(r"<img(?![^>]*\bloading=)", re.IGNORECASE)
        total = 0
        for dirpath, _dirs, files in os.walk(templates_root):
            for fname in files:
                if not fname.endswith(".html"):
                    continue
                path = os.path.join(dirpath, fname)
                with open(path, "r", encoding="utf-8") as fh:
                    text = fh.read()
                new_text, n = pattern.subn('<img loading="lazy" decoding="async"', text)
                if n:
                    total += n
                    if not self.dry:
                        with open(path, "w", encoding="utf-8") as fh:
                            fh.write(new_text)
                    rel = os.path.relpath(path, templates_root).replace(os.sep, "/")
                    self.stdout.write(f"  {rel}: {n} <img> tag(s)")
        if not total:
            self.stdout.write("  (all <img> tags already lazy)")
