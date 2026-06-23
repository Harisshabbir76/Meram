/*
 * CMS apply (public site). Runs on every page.
 *   - Shared overrides (page "__shared__") apply to repeated regions on EVERY page:
 *       * index strips:   [data-cms-shared-scope="name"] -> key "name-<imgIndex>"
 *       * regions:        [data-cms-shared="name"]       -> key "name|<relPath>"
 *   - Page overrides apply to this page only, matched by DOM path.
 *   - Text feeds the data-en / data-ar translation system; per-language block
 *     styles are re-applied whenever the visitor switches language.
 */
(function () {
    "use strict";

    function setStyle(el, prop, val) {
        if (val === null || val === "") el.style.removeProperty(prop);
        else el.style.setProperty(prop, val, "important");
    }

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

    function applyBlockToEl(el, b, registry) {
        if (!el) return;
        Object.keys(b.styles || {}).forEach(function (p) { setStyle(el, p, b.styles[p]); });
        if (b.image && el.tagName === "IMG") { el.src = b.image; el.removeAttribute("srcset"); }
        if (b.hero_media) applyHeroMedia(el, b.hero_type, b.hero_media);
        if (b.content_en != null) el.setAttribute("data-en", b.content_en);
        if (b.content_ar != null) el.setAttribute("data-ar", b.content_ar);
        var se = b.styles_en || {}, sa = b.styles_ar || {};
        if (Object.keys(se).length || Object.keys(sa).length) {
            var all = {};
            Object.keys(se).forEach(function (p) { all[p] = 1; });
            Object.keys(sa).forEach(function (p) { all[p] = 1; });
            registry.push({ el: el, en: se, ar: sa, allProps: Object.keys(all) });
        }
    }

    // A shared key resolves to (possibly many) elements across the page.
    function resolveShared(key) {
        var els = [];
        if (key.indexOf("|") >= 0) {                       // region|relPath
            var bar = key.indexOf("|"), region = key.slice(0, bar), rel = key.slice(bar + 1);
            document.querySelectorAll('[data-cms-shared="' + region + '"]').forEach(function (root) {
                var el; try { el = rel ? root.querySelector(rel) : root; } catch (e) { el = null; }
                if (el && !el.hasAttribute("data-cms-gallery")) els.push(el);
            });
        } else {                                           // scope-index (img strip)
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

    function getJSON(url) {
        return fetch(url, { credentials: "same-origin" })
            .then(function (r) { return r.json(); })
            .catch(function () { return null; });
    }

    function run() {
        var page = document.body.getAttribute("data-cms-page");
        var pShared = window.CMS_SHARED_DATA_URL ? getJSON(window.CMS_SHARED_DATA_URL) : Promise.resolve(null);
        var pPage = (page && window.CMS_DATA_URL) ? getJSON(window.CMS_DATA_URL) : Promise.resolve(null);

        Promise.all([pShared, pPage]).then(function (res) {
            var registry = [];
            var sharedData = res[0], pageData = res[1];

            if (sharedData && sharedData.blocks) {
                Object.keys(sharedData.blocks).forEach(function (key) {
                    resolveShared(key).forEach(function (el) { applyBlockToEl(el, sharedData.blocks[key], registry); });
                });
            }
            if (pageData && pageData.blocks) {
                Object.keys(pageData.blocks).forEach(function (key) {
                    var el; try { el = document.querySelector(key); } catch (e) { return; }
                    if (el) applyBlockToEl(el, pageData.blocks[key], registry);
                });
            }

            function applyLangStyles(lang) {
                registry.forEach(function (item) {
                    var set = lang === "ar" ? item.ar : item.en;
                    item.allProps.forEach(function (p) { item.el.style.removeProperty(p); });
                    Object.keys(set).forEach(function (p) { setStyle(item.el, p, set[p]); });
                });
            }
            if (typeof window.setLang === "function") {
                var orig = window.setLang;
                window.setLang = function (lang) { orig(lang); applyLangStyles(lang); };
            }
            var cur = localStorage.getItem("meramLang") || "en";
            if (typeof window.setLang === "function") window.setLang(cur);
            else applyLangStyles(cur);
        });
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
    else run();
})();
