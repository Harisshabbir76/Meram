/* ============================================================
   Visual Home Editor.

   Text styling (font / size / weight / colour / letter-spacing) applies to the
   exact text you SELECT inside the English or Arabic box — select part of the
   text to style only that part. Block styling (margin / padding / layout /
   align) applies per language to the whole element.
   ============================================================ */
(function () {
    "use strict";

    var PAGE = window.CMS_PAGE || "home";
    var EDITABLE = "h1,h2,h3,h4,h5,h6,p,span,a,li,blockquote,button,img,figcaption,small,strong,em,label";
    var bgType = "image";           // current hero-background media choice

    var selectedEl = null;
    var selectedKey = null;
    var selectedPage = PAGE;        // PAGE, or "__shared__" for cross-page shared elements
    var activeLang = "en";          // which box (en/ar) the user is working in
    var previewLang = localStorage.getItem("meramLang") || "en";  // language shown in the page preview
    var savedRange = null;          // last text selection inside a box
    var savedBox = null;
    var dirty = {};                 // { key: {content_en, content_ar, styles_en:{}, styles_ar:{}} }
    var loaded = {};                // server overrides, for populating fields

    /* ---------------------------------------------- DOM path key */
    function cmsPath(el) {
        if (!el || el.nodeType !== 1) return null;
        var parts = [], rooted = false;
        while (el && el.nodeType === 1 && el.tagName !== "BODY" && el.tagName !== "HTML") {
            if (el.id) {
                parts.unshift("#" + (window.CSS && CSS.escape ? CSS.escape(el.id) : el.id));
                rooted = true; break;
            }
            var parent = el.parentNode, sel = el.tagName.toLowerCase();
            if (parent) {
                var same = [];
                for (var i = 0; i < parent.children.length; i++)
                    if (parent.children[i].tagName === el.tagName) same.push(parent.children[i]);
                if (same.length > 1) sel += ":nth-of-type(" + (same.indexOf(el) + 1) + ")";
            }
            parts.unshift(sel);
            el = el.parentNode;
        }
        if (!rooted) parts.unshift("body");
        return parts.join(">");
    }

    /* ---------------------------------------------- shared (cross-page) elements */
    // Two shared kinds, both saved under page "__shared__":
    //   * index strip: an <img> inside [data-cms-shared-scope] -> key "scope-<idx>"
    //   * region:      any element inside [data-cms-shared]     -> key "region|<relPath>"
    // so the same edit applies on every page that has that region/strip.
    function relPathWithin(el, root) {
        var parts = [];
        while (el && el !== root && el.nodeType === 1) {
            var parent = el.parentNode, sel = el.tagName.toLowerCase();
            if (parent) {
                var same = [];
                for (var i = 0; i < parent.children.length; i++)
                    if (parent.children[i].tagName === el.tagName) same.push(parent.children[i]);
                if (same.length > 1) sel += ":nth-of-type(" + (same.indexOf(el) + 1) + ")";
            }
            parts.unshift(sel);
            el = el.parentNode;
        }
        return parts.join(">");
    }

    function sharedKeyFor(el) {
        if (!el || el.hasAttribute("data-cms-gallery")) return null;
        var scopeEl = el.tagName === "IMG" ? el.closest("[data-cms-shared-scope]") : null;
        if (scopeEl) {
            var idx = [].indexOf.call(scopeEl.querySelectorAll("img"), el);
            if (idx >= 0) return scopeEl.getAttribute("data-cms-shared-scope") + "-" + idx;
        }
        var region = el.closest("[data-cms-shared]");
        if (region && el !== region)
            return region.getAttribute("data-cms-shared") + "|" + relPathWithin(el, region);
        return null;
    }

    function resolveShared(key) {
        var els = [];
        if (key.indexOf("|") >= 0) {
            var bar = key.indexOf("|"), region = key.slice(0, bar), rel = key.slice(bar + 1);
            document.querySelectorAll('[data-cms-shared="' + region + '"]').forEach(function (root) {
                var el; try { el = rel ? root.querySelector(rel) : root; } catch (e) { el = null; }
                if (el && !el.hasAttribute("data-cms-gallery")) els.push(el);
            });
        } else {
            var dash = key.lastIndexOf("-"), scope = key.slice(0, dash), idx = parseInt(key.slice(dash + 1), 10);
            if (!isNaN(idx)) {
                document.querySelectorAll('[data-cms-shared-scope="' + scope + '"]').forEach(function (c) {
                    var el = c.querySelectorAll("img")[idx];
                    if (el && !el.hasAttribute("data-cms-gallery")) els.push(el);
                });
            }
        }
        return els;
    }

    function applySharedBlock(key, b) {
        resolveShared(key).forEach(function (el) {
            Object.keys(b.styles || {}).forEach(function (p) { setStyle(el, p, b.styles[p]); });
            Object.keys(b.styles_en || {}).forEach(function (p) { setStyle(el, p, b.styles_en[p]); });
            if (b.image && el.tagName === "IMG") { el.src = b.image; el.removeAttribute("srcset"); }
            if (b.hero_media) applyHeroMedia(el, b.hero_type, b.hero_media);
            if (b.content_en != null) { el.setAttribute("data-en", b.content_en); el.innerHTML = b.content_en; }
            if (b.content_ar != null) el.setAttribute("data-ar", b.content_ar);
        });
    }

    /* ---------------------------------------------- helpers */
    function $(id) { return document.getElementById(id); }
    function isEditorUI(node) { return !!(node && node.closest && node.closest("#cms-editor-root,#cms-topbar,#cms-hint")); }
    function setStyle(el, prop, val) {
        if (val === null || val === "" || val === undefined) el.style.removeProperty(prop);
        else el.style.setProperty(prop, val, "important");
    }

    /* Set a background to an image or a looping muted video. Works whether the
       background is a CSS-background element (div) OR an <img> tag covered by
       a text overlay. */
    function applyHeroMedia(el, type, url) {
        if (!el || !url) return;
        var isImg = el.tagName === "IMG";
        var container = isImg ? el.parentNode : el;
        if (container && getComputedStyle(container).position === "static")
            container.style.position = "relative";
        var vid = container.querySelector(":scope > video.cms-bg-video");
        if (type === "video") {
            if (isImg) el.style.display = "none"; else setStyle(el, "background-image", "none");
            if (!vid) {
                vid = document.createElement("video");
                vid.className = "cms-bg-video";
                vid.autoplay = true; vid.loop = true; vid.muted = true;
                vid.setAttribute("muted", ""); vid.setAttribute("playsinline", "");
                vid.style.cssText = "position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;";
                if (isImg) el.insertAdjacentElement("afterend", vid);
                else el.insertBefore(vid, el.firstChild);
            }
            if (vid.getAttribute("src") !== url) vid.setAttribute("src", url);
            if (vid.play) { var p = vid.play(); if (p && p.catch) p.catch(function () {}); }
        } else {
            if (vid) vid.remove();
            if (isImg) { el.style.display = ""; el.src = url; el.removeAttribute("srcset"); }
            else {
                setStyle(el, "background-image", 'url("' + url + '")');
                setStyle(el, "background-size", "cover");
                setStyle(el, "background-position", "center");
                setStyle(el, "background-repeat", "no-repeat");
            }
        }
    }
    function ensureDirty(key) {
        if (!dirty[key]) dirty[key] = { styles_en: {}, styles_ar: {}, __page: selectedPage };
        if (!dirty[key].styles_en) dirty[key].styles_en = {};
        if (!dirty[key].styles_ar) dirty[key].styles_ar = {};
        return dirty[key];
    }
    function markDirty() {
        var has = Object.keys(dirty).length > 0;
        $("cms-topbar-save").disabled = !has;
        $("cms-status").textContent = has ? "Unsaved changes" : "";
    }
    function styleKey() { return activeLang === "ar" ? "styles_ar" : "styles_en"; }
    function box(lang) { return $(lang === "ar" ? "cms-ar" : "cms-en"); }

    /* ---------------------------------------------- apply saved overrides */
    function applyOverrides() {
        if (!window.CMS_DATA_URL) return;
        fetch(window.CMS_DATA_URL, { credentials: "same-origin" })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                var blocks = (data && data.blocks) || {};
                Object.keys(blocks).forEach(function (key) {
                    var el; try { el = document.querySelector(key); } catch (e) { return; }
                    if (!el) return;
                    var b = blocks[key];
                    loaded[key] = { styles_en: b.styles_en || {}, styles_ar: b.styles_ar || {},
                                    hero_media: b.hero_media || null, hero_type: b.hero_type || "" };
                    Object.keys(b.styles || {}).forEach(function (p) { setStyle(el, p, b.styles[p]); });
                    if (b.image && el.tagName === "IMG") { el.src = b.image; el.removeAttribute("srcset"); }
                    if (b.hero_media) applyHeroMedia(el, b.hero_type, b.hero_media);
                    if (b.content_en != null) el.setAttribute("data-en", b.content_en);
                    if (b.content_ar != null) el.setAttribute("data-ar", b.content_ar);
                });
                // render text + block styles in the current preview language
                if (typeof window.setLang === "function") window.setLang(previewLang);
                else applyBlockForLang(previewLang);
            }).catch(function () {});

        // shared (cross-page) overrides, applied by scope+index
        if (window.CMS_SHARED_DATA_URL) {
            fetch(window.CMS_SHARED_DATA_URL, { credentials: "same-origin" })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    var blocks = (data && data.blocks) || {};
                    Object.keys(blocks).forEach(function (key) {
                        loaded[key] = blocks[key];
                        applySharedBlock(key, blocks[key]);
                    });
                }).catch(function () {});
        }
    }

    /* Apply the per-language block styles for `lang` to every overridden element. */
    function applyBlockForLang(lang) {
        var sk = lang === "ar" ? "styles_ar" : "styles_en";
        var ok = lang === "ar" ? "styles_en" : "styles_ar";
        Object.keys(loaded).forEach(function (key) {
            var el; try { el = document.querySelector(key); } catch (e) { return; }
            if (!el) return;
            var cur = Object.assign({}, loaded[key][sk] || {}, (dirty[key] && dirty[key][sk]) || {});
            var other = Object.assign({}, loaded[key][ok] || {}, (dirty[key] && dirty[key][ok]) || {});
            Object.keys(other).forEach(function (p) { if (!(p in cur)) el.style.removeProperty(p); });
            Object.keys(cur).forEach(function (p) { setStyle(el, p, cur[p]); });
        });
    }

    function updateLangSwitch() {
        document.querySelectorAll("#cms-lang-switch button").forEach(function (b) {
            b.classList.toggle("active", b.getAttribute("data-prev") === previewLang);
        });
    }

    /* ---------------------------------------------- fonts available in the project */
    // Local @font-face fonts (files under main/static/main/fonts/) + linked Google Fonts.
    var FONTS = [
        { label: "Dearest", value: "'Dearest'" },
        { label: "Charlotte", value: "'charlotte'" },
        { label: "FreightDisp Pro", value: "'FreightDisp Pro'" },
        { label: "Shabby Chic", value: "'Shabby Chic'" },
        { label: "Cormorant Garamond", value: "'Cormorant Garamond', serif" },
        { label: "Hanken Grotesk", value: "'Hanken Grotesk', sans-serif" },
        { label: "Montserrat", value: "'Montserrat', sans-serif" },
        { label: "Playfair Display", value: "'Playfair Display', serif" },
        { label: "Pinyon Script", value: "'Pinyon Script', cursive" },
        { label: "Noto Sans Arabic — عربي", value: "'Noto Sans Arabic', sans-serif" }
    ];

    /* ---------------------------------------------- rich-text toolbars */
    var TOOLS = [
        { type: "select", cmd: "formatBlock", title: "Text style", options: [
            ["P", "Paragraph"], ["H1", "H1"], ["H2", "H2"], ["H3", "H3"],
            ["H4", "H4"], ["H5", "H5"], ["H6", "H6"], ["BLOCKQUOTE", "Quote"] ]},
        { type: "font", title: "Font" },
        { type: "sep" },
        { type: "btn", cmd: "bold", html: "<b>B</b>", title: "Bold" },
        { type: "btn", cmd: "italic", html: "<i>I</i>", title: "Italic" },
        { type: "btn", cmd: "underline", html: "<u>U</u>", title: "Underline" },
        { type: "btn", cmd: "strikeThrough", html: "<s>S</s>", title: "Strikethrough" },
        { type: "sep" },
        { type: "btn", cmd: "justifyLeft", html: '<i class="fa-solid fa-align-left"></i>', title: "Align left" },
        { type: "btn", cmd: "justifyCenter", html: '<i class="fa-solid fa-align-center"></i>', title: "Align center" },
        { type: "btn", cmd: "justifyRight", html: '<i class="fa-solid fa-align-right"></i>', title: "Align right" },
        { type: "sep" },
        { type: "btn", cmd: "insertUnorderedList", html: '<i class="fa-solid fa-list-ul"></i>', title: "Bullet list" },
        { type: "btn", cmd: "insertOrderedList", html: '<i class="fa-solid fa-list-ol"></i>', title: "Numbered list" },
        { type: "btn", cmd: "createLink", html: '<i class="fa-solid fa-link"></i>', title: "Add link" },
        { type: "btn", cmd: "unlink", html: '<i class="fa-solid fa-link-slash"></i>', title: "Remove link" },
        { type: "sep" },
        { type: "color", cmd: "foreColor", title: "Text colour" },
        { type: "btn", cmd: "removeFormat", html: '<i class="fa-solid fa-eraser"></i>', title: "Clear formatting" }
    ];

    function buildToolbar(container) {
        var targetId = container.getAttribute("data-target");
        TOOLS.forEach(function (t) {
            var node;
            if (t.type === "sep") { node = document.createElement("span"); node.className = "cms-tb-sep"; }
            else if (t.type === "font") {
                node = document.createElement("select");
                node.title = t.title; node.className = "cms-font-select";
                var def = document.createElement("option"); def.value = ""; def.textContent = "Font"; node.appendChild(def);
                FONTS.forEach(function (f) {
                    var op = document.createElement("option");
                    op.value = f.value; op.textContent = f.label; op.style.fontFamily = f.value;
                    node.appendChild(op);
                });
                node.addEventListener("change", function () {
                    if (node.value) applyInline("font-family", node.value);
                    node.value = "";   // it's an action, not a state
                });
            }
            else if (t.type === "select") {
                node = document.createElement("select"); node.title = t.title;
                t.options.forEach(function (o) { var op = document.createElement("option"); op.value = o[0]; op.textContent = o[1]; node.appendChild(op); });
                node.addEventListener("change", function () { exec(targetId, t.cmd, node.value); });
            } else if (t.type === "color") {
                node = document.createElement("input"); node.type = "color"; node.title = t.title; node.value = "#1a1612";
                node.addEventListener("change", function () { exec(targetId, t.cmd, node.value); });
            } else {
                node = document.createElement("button"); node.type = "button"; node.innerHTML = t.html; node.title = t.title;
                node.addEventListener("mousedown", function (e) { e.preventDefault(); });
                node.addEventListener("click", function (e) {
                    e.preventDefault();
                    var val = null;
                    if (t.cmd === "createLink") { val = prompt("Link URL:", "https://"); if (!val) return; }
                    exec(targetId, t.cmd, val);
                });
            }
            container.appendChild(node);
        });
    }

    function exec(targetId, cmd, val) {
        var b = $(targetId);
        // capture the saved selection BEFORE focus (focus fires selectionchange)
        var r = (savedRange && b.contains(savedRange.commonAncestorContainer)) ? savedRange.cloneRange() : null;
        b.focus();
        if (r) { var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r); }
        document.execCommand("styleWithCSS", false, true);
        document.execCommand(cmd, false, val);
        mirrorBox(targetId);
    }

    function mirrorBox(targetId) {
        if (!selectedEl) return;
        var b = $(targetId), d = ensureDirty(selectedKey);
        if (targetId === "cms-en") {
            d.content_en = b.innerHTML;
            selectedEl.setAttribute("data-en", b.innerHTML);
            if (previewLang === "en") selectedEl.innerHTML = b.innerHTML;  // update live preview
        } else {
            d.content_ar = b.innerHTML;
            selectedEl.setAttribute("data-ar", b.innerHTML);
            if (previewLang === "ar") selectedEl.innerHTML = b.innerHTML;  // update live preview
        }
        markDirty();
    }

    /* ---------------------------------------------- selection tracking */
    function trackSelection() {
        var sel = window.getSelection();
        if (!sel.rangeCount) return;
        var r = sel.getRangeAt(0);
        var anchor = r.commonAncestorContainer;
        var elNode = anchor.nodeType === 1 ? anchor : anchor.parentElement;
        var b = elNode && elNode.closest ? elNode.closest("#cms-en,#cms-ar") : null;
        if (b) {
            savedRange = r.cloneRange();
            savedBox = b;
            setActiveLang(b.id === "cms-ar" ? "ar" : "en");
        }
    }
    /* ---------------------------------------------- inline text styling (selection) */
    function applyInline(prop, value) {
        var b = savedBox || box(activeLang);
        // Capture the target range BEFORE focusing (focus fires selectionchange,
        // which would overwrite savedRange and lose a partial selection).
        // Prefer a live, non-collapsed selection inside the box; fall back to the
        // last saved selection; finally fall back to the whole box.
        var range = null;
        var liveSel = window.getSelection();
        if (liveSel.rangeCount) {
            var lr = liveSel.getRangeAt(0);
            if (!lr.collapsed && b.contains(lr.commonAncestorContainer)) range = lr.cloneRange();
        }
        if (!range && savedRange && !savedRange.collapsed && b.contains(savedRange.commonAncestorContainer))
            range = savedRange.cloneRange();
        if (!range) { range = document.createRange(); range.selectNodeContents(b); }

        b.focus();
        var sel = window.getSelection();
        sel.removeAllRanges(); sel.addRange(range);

        if (value === "" || value === null) {
            // remove this property from any wrapping spans in the selection
            stripInlineProp(range, prop);
        } else {
            var span = document.createElement("span");
            span.style.setProperty(prop, value, "important");
            try {
                span.appendChild(range.extractContents());
                range.insertNode(span);
                sel.removeAllRanges();
                var nr = document.createRange(); nr.selectNodeContents(span);
                sel.addRange(nr); savedRange = nr.cloneRange(); savedBox = b;
            } catch (e) { /* selection spanned incompatible nodes */ }
        }
        mirrorBox(b.id);
    }

    function stripInlineProp(range, prop) {
        var frag = range.cloneContents();
        var holder = document.createElement("div");
        holder.appendChild(frag);
        holder.querySelectorAll("span").forEach(function (s) { s.style.removeProperty(prop); });
        range.deleteContents();
        var nodes = [].slice.call(holder.childNodes);
        nodes.reverse().forEach(function (n) { range.insertNode(n); });
    }

    /* ---------------------------------------------- block styling (per language) */
    function wireBlockInputs() {
        document.querySelectorAll("#cms-editor-root [data-style]").forEach(function (input) {
            input.addEventListener("input", function () {
                if (!selectedEl) return;
                var prop = input.getAttribute("data-style"), val = input.value;
                ensureDirty(selectedKey)[styleKey()][prop] = val;
                if (activeLang === previewLang) setStyle(selectedEl, prop, val); // live preview
                markDirty();
            });
        });
    }
    function wireInlineInputs() {
        document.querySelectorAll("#cms-editor-root [data-inline]").forEach(function (input) {
            var evt = input.type === "color" ? "change" : "change";
            input.addEventListener(evt, function () {
                if (!selectedEl) return;
                applyInline(input.getAttribute("data-inline"), input.value);
            });
        });
    }

    function populateBlockInputs() {
        var src = {};
        var sk = styleKey();
        if (loaded[selectedKey] && loaded[selectedKey][sk]) Object.assign(src, loaded[selectedKey][sk]);
        if (dirty[selectedKey] && dirty[selectedKey][sk]) Object.assign(src, dirty[selectedKey][sk]);
        document.querySelectorAll("#cms-editor-root [data-style]").forEach(function (input) {
            input.value = src[input.getAttribute("data-style")] || "";
        });
    }

    function setActiveLang(lang) {
        activeLang = lang;
        var tag = $("cms-lang-tag");
        if (tag) { tag.textContent = lang === "ar" ? "Arabic" : "English"; tag.classList.toggle("ar", lang === "ar"); }
        if (selectedEl) populateBlockInputs();
    }

    /* ---------------------------------------------- selection of a page element */
    function selectElement(el) {
        if (selectedEl) selectedEl.classList.remove("cms-selected-outline");
        selectedEl = el;
        var sharedKey = sharedKeyFor(el);
        if (sharedKey) { selectedKey = sharedKey; selectedPage = "__shared__"; }
        else { selectedKey = cmsPath(el); selectedPage = PAGE; }
        savedRange = null; savedBox = null;
        el.classList.add("cms-selected-outline");

        $("cms-key-label").textContent = selectedKey;
        $("cms-shared-badge").style.display = selectedPage === "__shared__" ? "" : "none";
        var isBg = el.hasAttribute("data-cms-bg");
        var isImg = !isBg && el.tagName === "IMG";

        $("cms-bg-section").style.display = isBg ? "" : "none";
        $("cms-text-section").style.display = (isBg || isImg) ? "none" : "";
        $("cms-image-section").style.display = isImg ? "" : "none";
        $("cms-style-sections").style.display = isBg ? "none" : "";

        if (isBg) {
            var info = loaded[selectedKey] || {};
            setBgType(info.hero_type || "image");
            var preview = info.hero_media || (el.tagName === "IMG" ? el.src : "");
            showBgPreview(info.hero_type || "image", preview);
        } else if (isImg) {
            $("cms-image-preview").src = el.src;
            var shared = el.hasAttribute("data-cms-gallery") || !!sharedKeyFor(el);
            $("cms-image-shared-note").style.display = shared ? "" : "none";
        } else {
            var en = el.getAttribute("data-en");
            $("cms-en").innerHTML = en != null ? en : el.innerHTML;
            $("cms-ar").innerHTML = el.getAttribute("data-ar") || "";
        }

        setActiveLang(previewLang);   // default editing to the language being previewed
        // reset inline controls (they are per-selection actions)
        $("cms-font-family") && ($("cms-font-family").value = "");
        $("cms-font-weight") && ($("cms-font-weight").value = "");
        $("cms-font-size") && ($("cms-font-size").value = "");
        $("cms-letter-spacing") && ($("cms-letter-spacing").value = "");
        $("cms-color") && ($("cms-color").value = toHex(getComputedStyle(el).color) || "#1a1612");
        if (!isBg) populateBlockInputs();

        var root = $("cms-editor-root");
        root.classList.add("open"); root.setAttribute("aria-hidden", "false");
    }

    function toHex(c) {
        if (!c) return null;
        if (c.charAt(0) === "#") return c.length === 7 ? c : null;
        var m = c.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
        if (!m) return null;
        function h(n) { return ("0" + parseInt(n, 10).toString(16)).slice(-2); }
        return "#" + h(m[1]) + h(m[2]) + h(m[3]);
    }

    /* ---------------------------------------------- image upload */
    function wireImageUpload() {
        var file = $("cms-image-file");
        file.addEventListener("change", function () {
            if (!file.files.length || !selectedEl) return;
            var galleryId = selectedEl.getAttribute("data-cms-gallery");
            var fd = new FormData();
            var url;
            if (galleryId) {
                // shared gallery image -> writes back to the DB record (all pages)
                fd.append("gallery_id", galleryId); fd.append("image", file.files[0]);
                url = window.CMS_GALLERY_URL;
            } else {
                // selectedPage is "__shared__" for shared-scope images, else the page
                fd.append("page", selectedPage); fd.append("element_key", selectedKey); fd.append("image", file.files[0]);
                url = window.CMS_IMAGE_URL;
            }
            $("cms-status").textContent = "Uploading…";
            fetch(url, { method: "POST", headers: { "X-CSRFToken": window.CMS_CSRF }, credentials: "same-origin", body: fd })
                .then(function (r) { return r.json(); }).then(function (res) {
                    if (res.ok) {
                        selectedEl.src = res.url; selectedEl.removeAttribute("srcset");
                        $("cms-image-preview").src = res.url;
                        $("cms-status").textContent = galleryId ? "Saved to all pages" : "Image saved";
                    } else { $("cms-status").textContent = "Upload failed"; }
                }).catch(function () { $("cms-status").textContent = "Upload failed"; });
            file.value = "";
        });
    }

    /* ---------------------------------------------- hero background (image / video) */
    function setBgType(type) {
        bgType = type === "video" ? "video" : "image";
        document.querySelectorAll("#cms-bg-type button").forEach(function (b) {
            b.classList.toggle("active", b.getAttribute("data-bgtype") === bgType);
        });
        var input = $("cms-bg-file");
        input.setAttribute("accept", bgType === "video" ? "video/*" : "image/*");
        $("cms-bg-upload-label").textContent = bgType === "video" ? "Upload video" : "Upload image";
    }

    function showBgPreview(type, url) {
        var img = $("cms-bg-preview-img"), vid = $("cms-bg-preview-video");
        if (type === "video" && url) {
            vid.src = url; vid.style.display = ""; img.style.display = "none";
        } else if (url) {
            img.src = url; img.style.display = ""; vid.style.display = "none";
        } else {
            img.removeAttribute("src"); img.style.display = "none"; vid.style.display = "none";
        }
    }

    function wireBgUpload() {
        document.querySelectorAll("#cms-bg-type button").forEach(function (b) {
            b.addEventListener("click", function () { setBgType(b.getAttribute("data-bgtype")); });
        });
        var file = $("cms-bg-file");
        file.addEventListener("change", function () {
            if (!file.files.length || !selectedEl) return;
            var fd = new FormData();
            fd.append("page", PAGE); fd.append("element_key", selectedKey);
            fd.append("media_type", bgType); fd.append("file", file.files[0]);
            $("cms-status").textContent = "Uploading…";
            fetch(window.CMS_BG_URL, { method: "POST", headers: { "X-CSRFToken": window.CMS_CSRF }, credentials: "same-origin", body: fd })
                .then(function (r) { return r.json(); }).then(function (res) {
                    if (res.ok) {
                        applyHeroMedia(selectedEl, res.type, res.url);
                        loaded[selectedKey] = loaded[selectedKey] || {};
                        loaded[selectedKey].hero_type = res.type;
                        loaded[selectedKey].hero_media = res.url;
                        showBgPreview(res.type, res.url);
                        $("cms-status").textContent = "Background saved";
                    } else { $("cms-status").textContent = "Upload failed"; }
                }).catch(function () { $("cms-status").textContent = "Upload failed"; });
            file.value = "";
        });
    }

    /* ---------------------------------------------- save / reset */
    function save() {
        if (!Object.keys(dirty).length) return;
        $("cms-status").textContent = "Saving…";
        // group changes by their page (current page vs "__shared__")
        var groups = {};
        Object.keys(dirty).forEach(function (k) {
            var d = dirty[k], pg = d.__page || PAGE, copy = {};
            Object.keys(d).forEach(function (f) { if (f !== "__page") copy[f] = d[f]; });
            (groups[pg] = groups[pg] || {})[k] = copy;
        });
        Promise.all(Object.keys(groups).map(function (pg) {
            return fetch(window.CMS_SAVE_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": window.CMS_CSRF },
                credentials: "same-origin",
                body: JSON.stringify({ page: pg, changes: groups[pg] })
            }).then(function (r) { return r.json(); });
        })).then(function (results) {
            if (results.every(function (r) { return r && r.ok; })) {
                Object.keys(dirty).forEach(function (k) {
                    loaded[k] = loaded[k] || { styles_en: {}, styles_ar: {} };
                    Object.assign(loaded[k].styles_en, dirty[k].styles_en || {});
                    Object.assign(loaded[k].styles_ar, dirty[k].styles_ar || {});
                });
                dirty = {}; markDirty();
                $("cms-status").textContent = "✓ Saved";
                setTimeout(function () { var s = $("cms-status"); if (s.textContent === "✓ Saved") s.textContent = ""; }, 2500);
            } else { $("cms-status").textContent = "Save failed"; }
        }).catch(function () { $("cms-status").textContent = "Save failed"; });
    }

    function resetElement() {
        if (!selectedKey) return;
        if (!confirm("Reset this element to its original content and styling?")) return;
        fetch(window.CMS_RESET_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": window.CMS_CSRF },
            credentials: "same-origin",
            body: JSON.stringify({ page: selectedPage, element_key: selectedKey })
        }).then(function () { location.reload(); });
    }

    /* ---------------------------------------------- page interaction */
    function resolveTarget(t) {
        if (!t || isEditorUI(t)) return null;
        var ed = t.closest(EDITABLE);
        if (ed && !ed.hasAttribute("data-cms-bg") && !isEditorUI(ed)) {
            // Find the outermost editable element if nested
            var parentEd = ed.parentElement ? ed.parentElement.closest(EDITABLE) : null;
            while (parentEd && !isEditorUI(parentEd)) {
                ed = parentEd;
                parentEd = ed.parentElement ? ed.parentElement.closest(EDITABLE) : null;
            }
            return ed;
        }
        var bg = t.closest("[data-cms-bg]");
        if (bg) return bg;
        var host = t.closest("[data-cms-hero]");
        if (host) { var inner = host.querySelector("[data-cms-bg]"); if (inner) return inner; }
        return ed || null;
    }

    function wirePageClicks() {
        document.addEventListener("mouseover", function (e) {
            var el = resolveTarget(e.target);
            if (el && el !== selectedEl) el.classList.add("cms-hover-outline");
        }, true);
        document.addEventListener("mouseout", function (e) {
            var el = resolveTarget(e.target);
            if (el) el.classList.remove("cms-hover-outline");
        }, true);
        document.addEventListener("click", function (e) {
            if (isEditorUI(e.target)) return;
            e.preventDefault(); e.stopPropagation();
            var el = resolveTarget(e.target);
            if (el) { el.classList.remove("cms-hover-outline"); selectElement(el); }
        }, true);
    }

    function closePanel() {
        var root = $("cms-editor-root");
        root.classList.remove("open"); root.setAttribute("aria-hidden", "true");
        if (selectedEl) selectedEl.classList.remove("cms-selected-outline");
        selectedEl = null; selectedKey = null;
    }

    /* ---------------------------------------------- init */
    function populateFontFamilySelect() {
        var ff = $("cms-font-family");
        if (!ff) return;
        ff.innerHTML = '<option value="">Default (inherit)</option>';
        FONTS.forEach(function (f) {
            var op = document.createElement("option");
            op.value = f.value; op.textContent = f.label; op.style.fontFamily = f.value;
            ff.appendChild(op);
        });
    }

    function init() {
        document.querySelectorAll(".cms-toolbar").forEach(buildToolbar);
        populateFontFamilySelect();
        wireBlockInputs();
        wireInlineInputs();
        wireImageUpload();
        wireBgUpload();
        wirePageClicks();

        document.addEventListener("selectionchange", trackSelection);

        ["cms-en", "cms-ar"].forEach(function (id) {
            var b = $(id);
            b.addEventListener("input", function () { mirrorBox(id); });
            b.addEventListener("focus", function () { setActiveLang(id === "cms-ar" ? "ar" : "en"); });
        });

        $("cms-save-btn").addEventListener("click", save);
        $("cms-topbar-save").addEventListener("click", save);
        $("cms-reset-btn").addEventListener("click", resetElement);
        $("cms-close-btn").addEventListener("click", closePanel);

        // Preview-language: wrap the site's setLang so any language change (top-bar
        // toggle OR the page's own footer switch) also re-applies block styles and
        // keeps the editor in sync. The Arabic version is then shown in the preview.
        var origSetLang = window.setLang;
        window.setLang = function (lang) {
            if (typeof origSetLang === "function") origSetLang(lang);
            previewLang = lang;
            applyBlockForLang(lang);
            updateLangSwitch();
            if (selectedEl) { setActiveLang(lang); }
        };
        document.querySelectorAll("#cms-lang-switch button").forEach(function (b) {
            b.addEventListener("click", function () { window.setLang(b.getAttribute("data-prev")); });
        });
        updateLangSwitch();

        window.addEventListener("beforeunload", function (e) {
            if (Object.keys(dirty).length) { e.preventDefault(); e.returnValue = ""; }
        });

        applyOverrides();
        setTimeout(function () { var h = $("cms-hint"); if (h) h.style.opacity = "0"; }, 4000);
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
})();
