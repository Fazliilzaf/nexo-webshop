/* ============================================================
   NEXO — Liquid Ritual · Shared JS helpers
   ============================================================ */

window.NEXO = window.NEXO || {};

NEXO.reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

/* Lerp helper for rAF-driven motion */
NEXO.lerp = function (a, b, t) {
  return a + (b - a) * t;
};

NEXO.clamp = function (v, min, max) {
  return Math.min(max, Math.max(min, v));
};

/* Smooth 0..1 progress through a range */
NEXO.progress = function (v, start, end) {
  return NEXO.clamp((v - start) / (end - start), 0, 1);
};

/* Ease for scrubbed motion (out-expo feel, scrub-safe) */
NEXO.easeOut = function (t) {
  return 1 - Math.pow(1 - t, 3);
};

/* rAF-throttled scroll/resize subscription */
NEXO.onFrame = function (fn) {
  var ticking = false;
  function request() {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        fn();
      });
    }
  }
  window.addEventListener("scroll", request, { passive: true });
  window.addEventListener("resize", request);
  return request; // call once to prime
};
