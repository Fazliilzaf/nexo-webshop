/* ============================================================
   NEXO — Liquid Ritual · Glass pointer response
   Tracks the pointer per glass surface and writes --gx/--gy so
   the specular light + caustic streak feel physical.
   Disabled under prefers-reduced-motion (static, still designed).
   ============================================================ */

(function () {
  if (NEXO.reducedMotion.matches) return;

  var surfaces = [];
  var raf = null;

  function collect() {
    surfaces = Array.prototype.slice.call(document.querySelectorAll(".glass"));
  }

  function onMove(event) {
    var x = event.clientX != null ? event.clientX : (event.touches && event.touches[0].clientX);
    var y = event.clientY != null ? event.clientY : (event.touches && event.touches[0].clientY);
    if (x == null || y == null) return;
    if (raf) return;
    raf = requestAnimationFrame(function () {
      raf = null;
      for (var i = 0; i < surfaces.length; i++) {
        var el = surfaces[i];
        var r = el.getBoundingClientRect();
        if (r.bottom < -80 || r.top > window.innerHeight + 80) continue;
        var gx = NEXO.clamp((x - r.left) / Math.max(r.width, 1), 0, 1);
        var gy = NEXO.clamp((y - r.top) / Math.max(r.height, 1), 0, 1);
        /* ease toward the pointer even when it is off-surface,
           so the light "leans" rather than snaps */
        el.style.setProperty("--gx", gx.toFixed(3));
        el.style.setProperty("--gy", gy.toFixed(3));
      }
    });
  }

  /* Device tilt: let the light answer the phone itself */
  function onTilt(event) {
    if (event.gamma == null || event.beta == null) return;
    var gx = NEXO.clamp(0.5 + event.gamma / 90, 0, 1);
    var gy = NEXO.clamp(0.5 + (event.beta - 45) / 90, 0, 1);
    for (var i = 0; i < surfaces.length; i++) {
      surfaces[i].style.setProperty("--gx", gx.toFixed(3));
      surfaces[i].style.setProperty("--gy", gy.toFixed(3));
    }
  }

  document.addEventListener("pointermove", onMove, { passive: true });
  window.addEventListener("deviceorientation", onTilt, { passive: true });
  document.addEventListener("shopify:section:load", collect);
  collect();
})();
