/* ============================================================
   NEXO — Liquid Ritual · Cart
   Shopify AJAX API + ritual completion logic.
   The cart knows the +1/+2/+3 system and says so.
   ============================================================ */

(function () {
  var root = document.querySelector("[data-cart]");
  if (!root) return;

  var panel = root.querySelector("[data-cart-panel]");
  var body = root.querySelector("[data-cart-body]");
  var foot = root.querySelector("[data-cart-foot]");
  var totalEl = root.querySelector("[data-cart-total]");
  var statusEl = root.querySelector("[data-cart-ritual-status]");
  var stepEls = root.querySelectorAll("[data-cart-step]");
  var locale = JSON.parse(
    root.querySelector("[data-cart-locale]").textContent
  );

  var STEPS = [
    { n: 1, handle: "lather-me-up" },
    { n: 2, handle: "mist-me-crazy" },
    { n: 3, handle: "whip-me-good" }
  ];

  var lastFocus = null;

  /* ---------------- drawer open/close ---------------- */

  function open() {
    lastFocus = document.activeElement;
    root.hidden = false;
    requestAnimationFrame(function () {
      root.classList.add("is-open");
    });
    document.documentElement.style.overflow = "hidden";
    panel.focus && panel.setAttribute("tabindex", "-1");
    panel.focus();
    document.addEventListener("keydown", onKey);
  }

  function close() {
    root.classList.remove("is-open");
    document.documentElement.style.overflow = "";
    document.removeEventListener("keydown", onKey);
    setTimeout(function () {
      root.hidden = true;
      if (lastFocus) lastFocus.focus();
    }, 450);
  }

  function onKey(e) {
    if (e.key === "Escape") {
      close();
      return;
    }
    /* focus trap: keep Tab inside the dialog while it is open */
    if (e.key !== "Tab") return;
    var focusables = panel.querySelectorAll(
      'a[href], button:not([disabled]), input, [tabindex]:not([tabindex="-1"])'
    );
    if (!focusables.length) return;
    var first = focusables[0];
    var last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  document.addEventListener("click", function (e) {
    var toggle = e.target.closest("[data-cart-toggle]");
    if (toggle) {
      e.preventDefault();
      refresh().then(open);
      return;
    }
    if (e.target.closest("[data-cart-close]")) close();
  });

  /* ---------------- ritual state ---------------- */

  function renderRitual(cart) {
    var ritualBlock = root.querySelector("[data-cart-ritual]");
    var handles = {};
    cart.items.forEach(function (item) {
      if (item.handle) handles[item.handle] = true;
    });
    var count = 0;
    STEPS.forEach(function (step) {
      var inCart = !!handles[step.handle];
      if (inCart) count++;
      for (var i = 0; i < stepEls.length; i++) {
        if (Number(stepEls[i].getAttribute("data-cart-step")) === step.n) {
          stepEls[i].classList.toggle("is-in", inCart);
        }
      }
    });
    /* accessory-only carts (e.g. just the brush) must not trigger
       ritual copy — the block only speaks when the ritual is in play
       or the cart is empty */
    ritualBlock.hidden = count === 0 && cart.item_count > 0;
    if (count === 3) {
      statusEl.textContent = locale.complete;
    } else {
      statusEl.textContent =
        locale.ofThree.replace("__COUNT__", count) + " " + locale["continue"] + " →";
    }
  }

  /* ---------------- rendering ---------------- */

  function money(cents) {
    return (cents / 100).toLocaleString(document.documentElement.lang || "sv", {
      style: "currency",
      currency: (window.Shopify && Shopify.currency && Shopify.currency.active) || "SEK"
    });
  }

  function render(cart) {
    renderRitual(cart);

    document.querySelectorAll("[data-cart-count]").forEach(function (el) {
      el.textContent = cart.item_count;
      el.setAttribute("data-empty", cart.item_count === 0 ? "true" : "false");
    });

    if (cart.item_count === 0) {
      body.innerHTML =
        '<div class="cart__empty"><p class="t-smoke">' + locale.empty + "</p></div>";
      foot.hidden = true;
      return;
    }

    foot.hidden = false;
    var html = '<ul class="cart__items">';
    cart.items.forEach(function (item) {
      html +=
        '<li class="cart__item" data-key="' + item.key + '">' +
        '<div class="cart__item-info">' +
        '<p class="cart__item-title">' + item.product_title + "</p>" +
        '<div class="cart__item-qty t-mono">' +
        '<button type="button" data-qty="-1" aria-label="−">−</button>' +
        "<span>" + item.quantity + "</span>" +
        '<button type="button" data-qty="1" aria-label="+">+</button>' +
        "</div>" +
        "</div>" +
        '<p class="t-mono">' + money(item.final_line_price) + "</p>" +
        "</li>";
    });
    html += "</ul>";
    body.innerHTML = html;
    totalEl.textContent = money(cart.total_price);
  }

  function refresh() {
    return fetch("/cart.js", { headers: { Accept: "application/json" } })
      .then(function (r) { return r.json(); })
      .then(render)
      .catch(function () {});
  }

  /* ---------------- add / update ---------------- */

  document.addEventListener("click", function (e) {
    var addBtn = e.target.closest("[data-add]");
    if (addBtn && !addBtn.disabled) {
      var variantId = addBtn.getAttribute("data-variant-id");
      if (!variantId) return;
      e.preventDefault();
      var label = addBtn.textContent;
      addBtn.disabled = true;
      addBtn.textContent = "…";
      fetch("/cart/add.js", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ id: Number(variantId), quantity: 1 })
      })
        .then(function (r) {
          if (!r.ok) throw new Error("add failed");
          return refresh();
        })
        .then(function () {
          addBtn.textContent = locale.added + " ✓";
          open();
          setTimeout(function () {
            addBtn.textContent = label;
            addBtn.disabled = false;
          }, 1800);
        })
        .catch(function () {
          addBtn.textContent = label;
          addBtn.disabled = false;
        });
      return;
    }

    var qtyBtn = e.target.closest("[data-qty]");
    if (qtyBtn) {
      var row = qtyBtn.closest("[data-key]");
      if (!row) return;
      var delta = Number(qtyBtn.getAttribute("data-qty"));
      var current = Number(row.querySelector(".cart__item-qty span").textContent);
      fetch("/cart/change.js", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ id: row.getAttribute("data-key"), quantity: current + delta })
      })
        .then(function () { return refresh(); })
        .catch(function () {});
    }
  });

  /* keep the header count honest on load */
  refresh();
})();
