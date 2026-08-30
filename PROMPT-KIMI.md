# NEXO — build us a webshop worth staring at

You are the design lead and the engineer. **NEXO is a small Swedish luxury
haircare brand and this is its flagship storefront.** We want people to land on
it and feel something before they read a word.

Everything you need is in this repository:

```
brand/tokens/brand-facts.json   the handful of things that are fixed
brand/logo/svg/                 the wordmark, four variants
brand/fonts/Buda-Light.*        the wordmark's typeface
brand/reference/                the printed label + the official colour chip
content/products.json           all three products: copy, ingredients, full INCI, SV + EN
OPEN-QUESTIONS.md               what nobody has decided yet — ask, don't invent
```

Read all of it before you plan anything.

---

## The brand

Three products, sold as one ritual: **+1 Lather Me Up** (shampoo, 250 ml),
**+2 Mist Me Crazy** (leave-in spray), **+3 Whip Me Good** (cream). Wash,
condition, protect. Made in Sweden. Vegan. Clean formulas the founder can
defend ingredient by ingredient — the full INCI list with plain-language
explanations is already written and sits in `content/products.json`.

The names are playful. The packaging is not: a matte black label, a griege
wordmark, and nothing else. **That contrast is the brand's personality** — do
something interesting with it.

---

## What we're trying to achieve

1. **A first impression that stops people.** Most haircare sites look
   interchangeable. Ours must not. Someone should screenshot it.
2. **Sell the ritual, not the bottle.** The bundle of all three is the offer
   that matters. Make the three-step logic feel inevitable.
3. **Earn trust through transparency.** We publish every ingredient and what it
   does. That is a genuine differentiator in this category — build it into
   something people actually want to explore, not a legal footnote.
4. **Convert on a phone.** Most of our traffic will be Instagram → phone →
   checkout. Whatever you design has to be *better* on a small screen, not
   merely survive there.
5. **Come back.** Accounts, order history, and subscriptions, because these are
   products people finish and rebuy.

---

## Your mandate: make it memorable

**This is the part we care about most.** Do not give us a competent, safe,
templated store. Take a real creative position and commit to it. Surprise us.

Things worth exploring — none of them required, all of them fair game:
an opening moment that earns the scroll · type used at a scale most shops are
too timid for · the ritual as a sequence you move through rather than a grid of
three cards · the ingredient library as the most beautiful page on the site ·
a cart that feels like part of the brand · texture, grain, material, light ·
a transition between pages that makes the site feel like one object.

Two honest warnings, because we will notice:

- **Don't reach for the default "premium" look** — a black page with a big
  serif and generous whitespace is what every AI-designed brand site becomes.
  If your first idea is that, keep going.
- **Wow has to survive contact with commerce.** A gorgeous page that makes the
  price hard to find, the add-to-cart ambiguous, or the checkout slow has
  failed. The boldness belongs in the atmosphere; the buying path stays
  obvious.

---

## The only things you may not change

These are facts about the brand, not design opinions:

- The **wordmark** — use the supplied SVGs, never re-typeset or recolour it
  beyond the four variants provided.
- **`#A8A09D`** is NEXO's colour. It has to be present and meaningful. Build
  whatever palette you like *around* it.
- The **product names** and the **+1 / +2 / +3** system.
- The product copy and ingredient data in `content/products.json` — cosmetics
  claims are regulated. You may rewrite marketing copy for tone; you may not
  invent an efficacy claim, certification, award or customer review.
- **Swedish and English** from day one, everything through locale files, no
  hardcoded strings.

Everything else — layout, palette, typography, motion, imagery, structure,
what the homepage even *is* — is yours.

---

## Technical scope

**Shopify Online Store 2.0, custom theme built from scratch.** Liquid, vanilla
JS, CSS. No Dawn fork, no theme framework. Shopify handles payments (Klarna,
Swish, card), VAT, shipping and inventory — you build everything the customer
sees.

Must exist: home · product pages · cart · brand story · the ritual · ingredient
library · customer accounts with order history · subscriptions (native selling
plans) · journal/blog · email capture · search · the usual legal pages.

Non-negotiable quality bar — this is where we will be strict:

- **WCAG 2.2 AA.** Full keyboard operation, visible focus, real contrast.
  Check your palette; don't assume it passes.
- **Lighthouse mobile ≥ 90 performance, 100 accessibility.** LCP under 2s,
  CLS under 0.05. If an effect costs more than it gives, cut the effect.
- `prefers-reduced-motion` honoured properly — not motion switched off, but a
  version of the design that still works still.
- Product/Offer/Organization JSON-LD, hreflang, real meta descriptions.
- Works on iOS Safari.

---

## How to start

**Do not write code yet.** First:

1. Read every file in this repository.
2. Come back with **two or three genuinely different creative directions** —
   a short written description each, and for each one: the idea in a sentence,
   what the homepage does, how the ritual is expressed, and what makes it
   memorable. Different *ideas*, not three palettes of the same idea.
3. Tell us which one you'd pick and why.
4. List what you need from us that isn't in the repo.

We'll choose a direction, then you build it — and we'd rather you defend a bold
call than hedge toward the middle.

Prices, product photography, two product volumes and our company details are
genuinely not decided yet — `OPEN-QUESTIONS.md` lists them. Use obvious
placeholders and flag them. Never fabricate a price.
