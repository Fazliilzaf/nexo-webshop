/* ============================================================
   NEXO — Liquid Ritual · Ingredient library interaction
   Progressive enhancement ONLY. Without this file the page is
   already complete: every explanation is open in the markup.
   With it: explanations collapse, the glass zone wakes up, and
   focus is driven by tap / keyboard / scroll-reading + search.
   ============================================================ */

(function () {
  var library = document.querySelector("[data-library]");
  if (!library) return;

  var reduce = NEXO.reducedMotion.matches;
  var index = library.querySelector("[data-library-index]");
  var zone = library.querySelector("[data-lens-zone]");
  var rows = Array.prototype.slice.call(library.querySelectorAll("[data-row]"));
  var toggles = library.querySelectorAll("[data-row-toggle]");
  var searchWrap = library.querySelector("[data-library-search]");
  var input = library.querySelector("[data-library-input]");
  var emptyNote = library.querySelector("[data-library-empty]");

  library.classList.add("is-live");
  if (searchWrap) searchWrap.hidden = false;

  /* ---------- focus model: one open row at a time ---------- */

  var focused = null;

  function setFocus(row, scrollTo) {
    if (focused === row) row = null; /* tap again to close */
    if (focused) focused.classList.remove("is-focus");
    focused = row;
    if (focused) {
      focused.classList.add("is-focus");
      if (scrollTo && !reduce) {
        var r = focused.getBoundingClientRect();
        var target = window.scrollY + r.top - window.innerHeight * 0.32;
        window.scrollTo({ top: target, behavior: "smooth" });
      }
    }
    syncAria();
  }

  function syncAria() {
    for (var i = 0; i < toggles.length; i++) {
      var row = toggles[i].closest("[data-row]");
      toggles[i].setAttribute("aria-expanded", row === focused ? "true" : "false");
    }
  }

  for (var i = 0; i < toggles.length; i++) {
    toggles[i].addEventListener("click", function () {
      setFocus(this.closest("[data-row]"), false);
    });
  }
  syncAria();

  /* ---------- the zone: brightens whatever it reads ---------- */

  if (zone && !reduce) {
    var zoneVisible = false;

    function updateReading() {
      var zr = zone.getBoundingClientRect();
      var zoneMid = zr.top + zr.height / 2;
      var section = index.getBoundingClientRect();
      var on = section.top < zr.top && section.bottom > zr.bottom;
      if (on !== zoneVisible) {
        zoneVisible = on;
        zone.classList.toggle("is-on", on);
      }
      if (!on) return;
      for (var i = 0; i < rows.length; i++) {
        if (rows[i].classList.contains("is-hidden")) continue;
        var r = rows[i].getBoundingClientRect();
        var reading = r.top < zoneMid && r.bottom > zoneMid - zr.height * 0.5;
        rows[i].classList.toggle("is-reading", reading);
      }
    }

    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        updateReading();
      });
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    updateReading();
  }

  /* ---------- search ---------- */

  if (input) {
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var visible = 0;
      for (var i = 0; i < rows.length; i++) {
        var hit = !q || rows[i].getAttribute("data-search").indexOf(q) !== -1;
        rows[i].classList.toggle("is-hidden", !hit);
        if (hit) visible++;
      }
      if (emptyNote) emptyNote.hidden = visible !== 0;
    });
  }
})();
