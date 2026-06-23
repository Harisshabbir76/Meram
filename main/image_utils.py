"""
Image optimization helpers.

Everything funnels through `encode_webp_bytes()` which:
  * honors EXIF orientation,
  * downscales so the longest side is <= MAX_SIDE,
  * re-encodes as WebP (preserving transparency when present).

`optimize_imagefield()` is used by model.save() so any image uploaded from the
dashboard is automatically shrunk + converted to .webp before it is stored.
The management command `optimize_images` reuses the same core for the existing
static files and already-uploaded media.
"""

import io
import os

from PIL import Image, ImageOps
from django.core.files.base import ContentFile

# HEIC / HEIF support (footer*.HEIC etc.)
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except Exception:  # pragma: no cover - optional
    pass

# Longest edge any image is allowed to keep. Hero images render full-width at
# ~1920px, so anything bigger is wasted bytes.
MAX_SIDE = 1920

# WebP quality. 80 is visually lossless for photos at typical screen sizes.
PHOTO_QUALITY = 80
ALPHA_QUALITY = 82

# Raster formats we know how to convert.
CONVERTIBLE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".bmp", ".tiff", ".gif"}


def _downscale(img):
    w, h = img.size
    longest = max(w, h)
    if longest > MAX_SIDE:
        scale = MAX_SIDE / float(longest)
        img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    return img


def encode_webp_bytes(fp, max_side=MAX_SIDE):
    """Return WebP-encoded bytes for the image at `fp` (path or file-like)."""
    with Image.open(fp) as img:
        img = ImageOps.exif_transpose(img)  # respect camera rotation
        img = _downscale(img)

        has_alpha = img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        )

        if has_alpha:
            img = img.convert("RGBA")
            quality = ALPHA_QUALITY
        else:
            img = img.convert("RGB")
            quality = PHOTO_QUALITY

        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=quality, method=6)
        return buf.getvalue()


def webp_name(original_name):
    """gallery/foo.JPG -> gallery/foo.webp (keeps the upload_to folder)."""
    root, _ = os.path.splitext(original_name)
    return root + ".webp"


def optimize_imagefield(field):
    """
    Convert a Django ImageField's current file to WebP in-place.

    Returns (new_basename, ContentFile) ready for `field.save(name, content,
    save=False)`, or None when nothing needs doing (already webp / empty).
    """
    if not field or not getattr(field, "name", ""):
        return None
    if field.name.lower().endswith(".webp"):
        return None

    # Read the raw bytes whether it's a fresh upload or a stored file.
    field.open("rb")
    try:
        data = encode_webp_bytes(field.file)
    finally:
        try:
            field.close()
        except Exception:
            pass

    base = os.path.splitext(os.path.basename(field.name))[0]
    return base + ".webp", ContentFile(data)


def optimize_instance_images(instance, field_names):
    """Convert every named ImageField on `instance` to WebP (pre-save)."""
    for name in field_names:
        field = getattr(instance, name, None)
        result = optimize_imagefield(field)
        if result:
            new_name, content = result
            field.save(new_name, content, save=False)
