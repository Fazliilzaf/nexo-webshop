/* ============================================================
   NEXO — Liquid Ritual · Homepage scroll engine
   One rAF loop scrubs:
     1. the pinned +1 → +2 → +3 ritual stage (with per-material
        physical character + pointer parallax + seam sweep)
     2. the bundle convergence (steps snap into a system)
     3. the ingredient lens drift
   Transforms + opacity only. No per-frame layout reads.
   ============================================================ */

(function () {
  function ss(a, b, x) {
    var t = NEXO.clamp((x - a) / (b - a), 0, 1);
    return t * t * (3 - 2 * t);
  }

  var reduce = NEXO.reducedMotion.matches;

  var ritual = document.querySelector("[data-ritual]");
  var bundle = document.querySelector("[data-bundle]");
  var scrubbers = [];

  /* ------------------------------------------------ ritual */

  if (ritual && !reduce) {
    ritual.classList.remove("ritual--static");

    var track = ritual.querySelector("[data-ritual-track]");
    var sweep = ritual.querySelector("[data-ritual-sweep]");
    var railItems = ritual.querySelectorAll("[data-rail-step]");
    var begin = ritual.querySelector("[data-ritual-begin]");

    /* Physical character per step:
       lather — soft, airborne, milky: floats up, near-full presence
       mist   — light, diffuse, atmospheric: drifts sideways, thins out
       whip   — dense, slow, creamy: heavy, barely moves, full mass */
    var CHAR = [
      { dx: 0, dy: -1, amp: 4.5, ceiling: 1.0, par: 1.2 },
      { dx: 1.3, dy: -0.25, amp: 5, ceiling: 0.66, par: 2.1 },
      { dx: 0, dy: 0.4, amp: 1.8, ceiling: 1.0, par: 0.7 }
    ];

    var steps = Array.prototype.map.call(
      ritual.querySelectorAll(".ritual__step"),
      function (el, i) {
        return {
          el: el,
          material: el.querySelector(".ritual__material"),
          body: el.querySelector(".ritual__body"),
          info: el.querySelector(".ritual__info"),
          char: CHAR[i]
        };
      }
    );

    var geo = { top: 0, total: 1 };
    var lastActive = 0;
    var entranceCleared = false;

    function clearEntrance() {
      /* CSS entrance animations hold fill:both — once the user scrolls,
         hand control back to the scrub engine */
      entranceCleared = true;
      var els = ritual.querySelectorAll(
        '.ritual__step[data-step="1"] .ritual__name-line, ' +
        '.ritual__step[data-step="1"] .ritual__info, ' +
        ".ritual__begin"
      );
      for (var i = 0; i < els.length; i++) els[i].style.animation = "none";
    }

    /* pointer parallax state (-1..1, lerped in the main loop) */
    var pointer = { x: 0, y: 0, tx: 0, ty: 0 };
    document.addEventListener(
      "pointermove",
      function (e) {
        pointer.tx = (e.clientX / window.innerWidth) * 2 - 1;
        pointer.ty = (e.clientY / window.innerHeight) * 2 - 1;
        kick();
      },
      { passive: true }
    );

    function measureRitual() {
      var rect = track.getBoundingClientRect();
      geo.top = rect.top + window.scrollY;
      geo.total = Math.max(rect.height - window.innerHeight, 1);
    }

    scrubbers.push({
      measure: measureRitual,
      active: function () {
        return (
          window.scrollY > geo.top - window.innerHeight &&
          window.scrollY < geo.top + geo.total + window.innerHeight
        );
      },
      value: function () {
        return NEXO.clamp((window.scrollY - geo.top) / geo.total, 0, 1);
      },
      tick: function () {
        pointer.x = NEXO.lerp(pointer.x, pointer.tx, 0.06);
        pointer.y = NEXO.lerp(pointer.y, pointer.ty, 0.06);
      },
      render: function (seg) {
        /* seg: 0..3 continuous position through the three steps */
        if (!entranceCleared && seg > 0.002) clearEntrance();
        for (var i = 0; i < steps.length; i++) {
          var s = steps[i];
          var c = s.char;
          var local = seg - i;
          var lc = NEXO.clamp(local, 0, 1);
          /* step 1 rests settled at page top; step 3 rests settled at
             the end — only the middle of the journey is "in transit" */
          var lt = lc;
          if (i === 0) lt = 0.5 + 0.5 * lc;
          if (i === steps.length - 1) lt = 0.5 * lc;

          var inOp = i === 0 ? 1 : ss(-0.06, 0.18, local);
          var outOp = i === steps.length - 1 ? 1 : 1 - ss(0.78, 1.06, local);
          var op = Math.min(inOp, outOp);

          s.el.classList.toggle("is-visible", op > 0.004);
          if (op <= 0.004) continue;

          /* material: character drift + pointer parallax */
          var transit = (lt - 0.5) * 2; /* -1..1 through the step's life */
          var mx = c.dx * c.amp * transit + pointer.x * c.par;
          var my = -c.dy * c.amp * transit + pointer.y * c.par * 0.7;
          var scale = 1.08 - 0.08 * lc;
          s.material.style.opacity = (op * c.ceiling).toFixed(3);
          s.material.style.transform =
            "scale(" + scale.toFixed(4) + ") translate3d(" +
            mx.toFixed(2) + "vh," + my.toFixed(2) + "vh,0)";

          /* body: enters from below, leaves upward */
          var bodyIn = i === 0 ? 1 : ss(-0.02, 0.26, local);
          var bodyOut = i === steps.length - 1 ? 1 : 1 - ss(0.74, 1.02, local);
          s.body.style.opacity = Math.min(bodyIn, bodyOut).toFixed(3);
          s.body.style.transform =
            "translate3d(0," + ((0.5 - lt) * 11).toFixed(2) + "vh,0)";

          /* dock: lags the body, compresses at the seams */
          var edge = ss(0.3, 0.5, Math.abs(lt - 0.5));
          var infoY = (0.5 - lt) * 18 + edge * 2.5;
          s.info.style.transform =
            "translate3d(0," + infoY.toFixed(2) + "vh,0) scale(" +
            (1 - edge * 0.045).toFixed(4) + ")";
        }

        /* seam sweep: darkness pulses as one world becomes the next */
        if (sweep) {
          var nearInt = Math.abs(seg - Math.round(seg));
          var inRange = ss(0.15, 0.5, seg) * (1 - ss(2.5, 2.85, seg));
          sweep.style.opacity =
            (ss(0.14, 0.02, nearInt) * 0.42 * inRange).toFixed(3);
        }

        var active = NEXO.clamp(Math.round(seg - 0.5) + 1, 1, 3);
        if (active !== lastActive) {
          lastActive = active;
          for (var r = 0; r < railItems.length; r++) {
            var n = r + 1;
            railItems[r].classList.toggle("is-active", n === active);
            railItems[r].classList.toggle("is-done", n < active);
            if (n === active) railItems[r].setAttribute("aria-current", "step");
            else railItems[r].removeAttribute("aria-current");
          }
        }

        if (begin) begin.style.opacity = (1 - ss(0.02, 0.16, seg)).toFixed(3);
      }
    });
  }

  /* ------------------------------------------------ bundle */

  if (bundle && !reduce) {
    var bTrack = bundle.querySelector("[data-bundle-track]");
    var bChips = bundle.querySelectorAll("[data-chip]");
    var bCore = bundle.querySelector("[data-bundle-core]");
    var bGroup = bundle.querySelector("[data-bundle-group]");
    var bLockline = bundle.querySelector("[data-bundle-lockline]");
    var bGlow = bundle.querySelector("[data-bundle-glow]");
    var bGeo = { top: 0, total: 1 };
    var vw = window.innerWidth, vh = window.innerHeight;

    /* where each chip starts, as viewport fractions */
    var origins = [
      { x: -0.38, y: -0.24, r: -7 },
      { x: 0.42, y: 0.05, r: 5 },
      { x: -0.2, y: 0.32, r: -4 }
    ];

    function measureBundle() {
      var rect = bTrack.getBoundingClientRect();
      bGeo.top = rect.top + window.scrollY;
      bGeo.total = Math.max(rect.height - window.innerHeight, 1);
      vw = window.innerWidth;
      vh = window.innerHeight;
    }

    scrubbers.push({
      measure: measureBundle,
      active: function () {
        return (
          window.scrollY > bGeo.top - vh &&
          window.scrollY < bGeo.top + bGeo.total + vh
        );
      },
      value: function () {
        return NEXO.clamp((window.scrollY - bGeo.top) / bGeo.total, 0, 1);
      },
      render: function (p) {
        /* 1. chips fly in        2. they SNAP into the label index
           3. the hairline draws  4. the index morphs into the core pane */
        var snap = ss(0.42, 0.52, p);
        var converge = ss(0, 0.52, p) * 0.92 + snap * 0.08;
        var drawn = ss(0.46, 0.62, p); /* lockline */
        var handoff = ss(0.56, 0.72, p); /* chips become the pane */
        var coreIn = NEXO.easeOut(ss(0.62, 0.92, p));

        for (var i = 0; i < bChips.length; i++) {
          var o = origins[i];
          var stackY = (i - 1) * 0.095 * vh;
          var x = NEXO.lerp(o.x * vw, 0, converge);
          var y = NEXO.lerp(o.y * vh, stackY, converge);
          var rot = NEXO.lerp(o.r, 0, converge);
          /* a 4% settle pulse as the snap lands */
          var settle = 1 + Math.sin(snap * Math.PI) * 0.04;
          bChips[i].style.opacity = (1 - handoff).toFixed(3);
          bChips[i].style.transform =
            "translate(-50%,-50%) translate3d(" + x.toFixed(1) + "px," +
            y.toFixed(1) + "px,0) rotate(" + rot.toFixed(2) + "deg) scale(" +
            (NEXO.lerp(1, 0.94, converge) * settle).toFixed(4) + ")";
        }

        if (bLockline) {
          bLockline.style.transform =
            "translate(-50%,-50%) scaleY(" + drawn.toFixed(3) + ")";
          bLockline.style.opacity = (drawn * (1 - handoff) * 0.7).toFixed(3);
        }

        if (bGlow) bGlow.style.opacity = (coreIn * 0.85).toFixed(3);

        /* the core grows OUT of the stacked index — morph, not fade-in */
        bCore.style.opacity = coreIn.toFixed(3);
        bCore.style.transform =
          "translate3d(0," + ((1 - coreIn) * 3).toFixed(2) + "vh,0) scale(" +
          NEXO.lerp(0.52, 1, coreIn).toFixed(4) + ")";
        bCore.style.visibility = coreIn > 0.004 ? "visible" : "hidden";

        if (bGroup) bGroup.style.opacity = (ss(0.7, 1, p) * 0.22).toFixed(3);
      }
    });
  }

  /* ------------------------------------------- scroll loop */

  var kick = function () {};

  if (scrubbers.length) {
    var current = scrubbers.map(function () { return 0; });
    var rafId = null;

    function frame() {
      rafId = null;
      var anyMoving = false;
      for (var i = 0; i < scrubbers.length; i++) {
        if (!scrubbers[i].active()) continue;
        if (scrubbers[i].tick) scrubbers[i].tick();
        var target = scrubbers[i].value();
        var v = NEXO.lerp(current[i], target, 0.16);
        if (Math.abs(v - target) < 0.0004) v = target;
        else anyMoving = true;
        current[i] = v;
        scrubbers[i].render(scrubbers[i] === scrubbers[0] ? v * 3 : v);
      }
      /* parallax keeps the loop alive briefly after scrolling stops */
      if (anyMoving) rafId = requestAnimationFrame(frame);
    }

    kick = function () {
      if (!rafId) rafId = requestAnimationFrame(frame);
    };

    function measureAll() {
      for (var i = 0; i < scrubbers.length; i++) scrubbers[i].measure();
      kick();
    }

    window.addEventListener("scroll", kick, { passive: true });
    window.addEventListener("resize", measureAll);
    measureAll();
  }

  /* ---------------------------------------- ingredient lens */

  var lens = document.querySelector("[data-lens]");
  if (lens && !reduce) {
    var flow = lens.querySelector("[data-lens-flow]");
    var items = flow.querySelectorAll("[data-lens-item]");
    var half = 0;
    var offset = 0;
    var dragging = false;
    var dragX = 0;
    var dragOffset = 0;

    function measureLens() {
      half = flow.scrollWidth / 2;
    }

    function lensFrame() {
      if (!dragging) offset -= 0.35; /* slow drift, px/frame */
      if (offset <= -half) offset += half;
      if (offset > 0) offset -= half;
      flow.style.transform = "translate3d(" + offset.toFixed(1) + "px,0,0)";

      /* focus the name nearest the lens centre */
      var centre = lens.getBoundingClientRect().left + lens.offsetWidth / 2;
      var best = null, bestDist = 1e9;
      for (var i = 0; i < items.length; i++) {
        var r = items[i].getBoundingClientRect();
        var d = Math.abs(r.left + r.width / 2 - centre);
        if (d < bestDist) { bestDist = d; best = items[i]; }
        items[i].classList.remove("is-focus");
      }
      if (best && bestDist < 220) best.classList.add("is-focus");
    }

    flow.style.touchAction = "pan-y";
    lens.addEventListener("pointerdown", function (e) {
      dragging = true;
      dragX = e.clientX;
      dragOffset = offset;
      lens.setPointerCapture(e.pointerId);
    });
    lens.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      offset = dragOffset + (e.clientX - dragX);
    });
    ["pointerup", "pointercancel"].forEach(function (ev) {
      lens.addEventListener(ev, function () { dragging = false; });
    });

    (function loop() {
      lensFrame();
      requestAnimationFrame(loop);
    })();
    window.addEventListener("resize", measureLens);
    measureLens();
  }
})();
