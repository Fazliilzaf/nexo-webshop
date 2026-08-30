/* Dev-only preview renderer.
   Renders the Shopify theme (theme/) to a static preview/index.html
   using liquidjs with mocked Shopify globals. NOT part of the theme. */

const fs = require("fs");
const path = require("path");
const { Liquid, Tag, TokenKind } = require("liquidjs");

const ROOT = path.resolve(__dirname, "..");
const THEME = path.join(ROOT, "theme");

const localeName = process.argv[2] === "en" ? "en" : "sv";
const localeFile =
  localeName === "en" ? "en.json" : "sv.default.json";
const STRINGS = JSON.parse(
  fs.readFileSync(path.join(THEME, "locales", localeFile), "utf8")
);

function lookup(key) {
  return key.split(".").reduce((acc, part) => {
    if (acc == null) return undefined;
    return acc[part];
  }, STRINGS);
}

function interpolate(str, params) {
  return str.replace(/\{\{\s*(\w+)\s*\}\}/g, (_, name) =>
    params && params[name] != null ? params[name] : `{{ ${name} }}`
  );
}

/* --- mocked Shopify globals --- */

const globals = {
  page_title: "NEXO — Liquid Ritual",
  page_description:
    "NEXO är svensk lyxig hårvård i tre steg: +1 rengör, +2 vårdar, +3 skyddar.",
  current_page: 1,
  content_for_header: "",
  template: { name: "index" },
  shop: {
    name: "NEXO",
    published_locales: [
      { iso_code: "sv", primary: true, root_url: "/" },
      { iso_code: "en", primary: false, root_url: "/en" }
    ]
  },
  request: {
    locale: { iso_code: localeName },
    origin: "http://localhost:8000",
    path: "/",
    design_mode: false
  },
  routes: {
    root_url: "/",
    cart_url: "/cart",
    all_products_collection_url: "/collections/all"
  },
  cart: { item_count: 0, items: [], total_price: 0 },
  all_products: {},
  settings: {},
  form: null
};

const engine = new Liquid({
  root: [path.join(THEME, "snippets"), path.join(THEME, "sections")],
  extname: ".liquid",
  strictVariables: false,
  strictFilters: false,
  globals /* engine-level: partials rendered via {% render %} see these too */
});

/* --- filters --- */
engine.registerFilter("t", (key, ...args) => {
  const hit = lookup(key);
  if (hit == null) return `[missing: ${key}]`;
  /* liquidjs passes named filter args as [name, value] pairs */
  const params = args.length ? Object.fromEntries(args) : undefined;
  return interpolate(String(hit), params);
});
engine.registerFilter("asset_url", (name) => `../theme/assets/${name}`);
engine.registerFilter(
  "stylesheet_tag",
  (url) => `<link rel="stylesheet" href="${url}">`
);
engine.registerFilter("money", (cents) => {
  const n = (Number(cents) / 100).toLocaleString("sv-SE", {
    style: "currency",
    currency: "SEK"
  });
  return n;
});
engine.registerFilter("json", (v) => JSON.stringify(v));
engine.registerFilter("handle", (v) =>
  String(v).toLowerCase().replace(/[^a-z0-9]+/g, "-")
);
engine.registerFilter("image_url", (src, ...args) => src);

/* --- custom tags: schema (drop), section (render file), form (wrap) --- */
class SchemaTag extends Tag {
  constructor(token, remainTokens, liquid) {
    super(token, remainTokens, liquid);
    while (remainTokens.length) {
      const t = remainTokens.shift();
      if (t.kind === TokenKind.Tag && t.name === "endschema") break;
    }
  }
  *render() {}
}

class SectionTag extends Tag {
  constructor(token, remainTokens, liquid) {
    super(token, remainTokens, liquid);
    this.file = token.args.trim().replace(/^['"]|['"]$/g, "");
    this.liquid = liquid;
  }
  *render(ctx) {
    const tpl = this.liquid.parse(
      fs.readFileSync(path.join(THEME, "sections", this.file + ".liquid"), "utf8")
    );
    return yield this.liquid.renderer.renderTemplates(tpl, ctx);
  }
}

class FormTag extends Tag {
  constructor(token, remainTokens, liquid) {
    super(token, remainTokens, liquid);
    this.templates = [];
    const stream = liquid.parser.parseStream(remainTokens);
    stream
      .on("tag:endform", () => stream.stop())
      .on("template", (tpl) => this.templates.push(tpl))
      .start();
  }
  *render(ctx) {
    const body = yield this.liquid.renderer.renderTemplates(this.templates, ctx);
    return `<form method="post" action="#">${body}</form>`;
  }
}

engine.registerTag("schema", SchemaTag);
engine.registerTag("section", SectionTag);
engine.registerTag("form", FormTag);

async function main() {
  const arg = process.argv[2];
  const mode =
    arg === "product" ? "product"
    : arg === "ingredients" ? "ingredients"
    : arg === "brand" ? "brand"
    : arg === "journal" ? "journal"
    : arg === "article" ? "article"
    : "index";
  const handle = process.argv[3] || "lather-me-up";

  /* homepage sections, in template order */
  const tplFile =
    mode === "product" ? "product.json"
    : mode === "ingredients" ? "page.ingredients.json"
    : mode === "brand" ? "page.brand.json"
    : mode === "journal" ? "blog.json"
    : mode === "article" ? "article.json"
    : "index.json";
  const tpl = JSON.parse(
    fs.readFileSync(path.join(THEME, "templates", tplFile), "utf8")
  );

  const catalog = JSON.parse(
    fs.readFileSync(path.join(ROOT, "content", "products.json"), "utf8")
  );

  function buildProduct(h) {
    if (h === "borste") {
      /* synthetic accessory mock — the brush has no entry in
         content/products.json (no INCI, no ritual step) */
      return {
        handle: "borste",
        title: "NEXO Borste",
        vendor: "NEXO",
        price: 0,
        available: true,
        url: "/products/borste",
        description: "",
        images: [],
        selected_or_first_available_variant: null,
        metafields: { nexo: {} }
      };
    }
    const entry = catalog.products.find((p) => p.handle === h);
    const sv = entry.sv;
    const volume =
      h === "lather-me-up" ? "250 ml" : h === "mist-me-crazy" ? "100 ml" : "30 ml";
    return {
      handle: h,
      title: sv.name,
      vendor: "NEXO",
      price: 0,
      available: true,
      url: "/products/" + h,
      description: sv.description,
      images: [],
      selected_or_first_available_variant: null,
      metafields: {
        nexo: {
          tagline: { value: sv.tagline },
          volume: { value: volume },
          key_ingredients: { value: sv.keyIngredients },
          inci: { value: sv.inci }
          /* usage intentionally unset → locale fallback path is tested */
        }
      }
    };
  }

  let pageGlobals = {};
  if (mode === "product") {
    pageGlobals = {
      template: { name: "product" },
      product: buildProduct(handle)
    };
  } else if (mode === "brand") {
    pageGlobals = {
      template: { name: "page", suffix: "brand" }
    };
  } else if (mode === "journal" || mode === "article") {
    /* DEV-ONLY fixtures: content built solely from approved material
       (usage texts, transparency facts, products.json explanations).
       Real articles are written in Shopify admin. */
    const articles = [
      {
        title: "Så bygger du ritualen: +1, +2, +3",
        handle: "sa-bygger-du-ritualen",
        url: "/blogs/journal/sa-bygger-du-ritualen",
        published_at: "2026-08-30",
        tags: ["RITUAL", "HOW-TO"],
        excerpt: "Tvätta, vårda, skydda — i den ordningen. Så får varje steg rätt förutsättningar.",
        content:
          "<p>Tre produkter, en ordning. Ritualen börjar med rengöring, fortsätter med vård och avslutas med skydd. Ordningen är inte ett förslag — den är själva idén.</p>" +
          "<h2>+1 Rengör</h2><p>Massera försiktigt in i fuktigt hår och hårbotten tills det bildas ett mjukt lödder. Skölj noggrant. Upprepa vid behov.</p>" +
          "<h2>+2 Vårda</h2><p>Spraya jämnt från cirka 10–15 cm avstånd. Låt torka eller massera försiktigt in. Fungerar i både fuktigt och torrt hår.</p>" +
          "<h2>+3 Skydda</h2><p>Använd dagligen vid behov. Arbeta in en liten mängd i hårbotten eller på torr hud.</p>",
        metafields: { nexo: {} }
      },
      {
        title: "Varför vi publicerar varje ingrediens",
        handle: "varfor-vi-publicerar-varje-ingrediens",
        url: "/blogs/journal/varfor-vi-publicerar-varje-ingrediens",
        published_at: "2026-08-30",
        tags: ["PHILOSOPHY", "INGREDIENTS"],
        excerpt: "Transparens är inte en fotnot. Det är hela affärsidén.",
        content:
          "<p>De flesta ingredienslistor är skrivna för att uppfylla ett lagkrav. Våra är skrivna för att läsas.</p>" +
          "<p>Varje ingrediens i alla tre steg är publicerad, med en förklaring på vanlig svenska. Inte för att det är enklast — utan för att en formula du kan försvara ingrediens för ingrediens är en formula värd att köpa.</p>" +
          "<blockquote>Om du inte kan förklara vad en ingrediens gör där, ska den inte vara där.</blockquote>",
        metafields: { nexo: {} }
      },
      {
        title: "Panthenol, på vanlig svenska",
        handle: "panthenol-pa-vanlig-svenska",
        url: "/blogs/journal/panthenol-pa-vanlig-svenska",
        published_at: "2026-08-30",
        tags: ["INGREDIENTS", "HAIR"],
        excerpt: "Provitamin B5 finns i alla tre stegen. Det är därför.",
        content:
          "<p>Panthenol — provitamin B5 — återkommer i hela ritualen. I INCI-listan är namnet tekniskt. Funktionen är enkel: det hjälper håret att kännas mjukt, slätt och glansfullt.</p>" +
          "<p>I +1 bidrar det till en glansfull, välmående look. I +2 hjälper det håret att kännas mjukt och välvårdat. I +3 verkar det lugnande och återfuktande. Samma ingrediens, tre roller — en av 43 som alla finns förklarade i ingrediensbiblioteket.</p>",
        metafields: { nexo: {} }
      }
    ];
    const journalBlog = {
      title: "Journal",
      handle: "journal",
      url: "/blogs/journal",
      articles
    };
    pageGlobals = {
      template: { name: mode === "journal" ? "blog" : "article" },
      blog: journalBlog
    };
    if (mode === "article") {
      const picked = articles.find((a) => a.handle === process.argv[3]) || articles[0];
      picked.metafields.nexo.product = { value: buildProduct("lather-me-up") };
      pageGlobals.article = picked;
    }
  } else if (mode === "ingredients") {    const functionsDoc = JSON.parse(
      fs.readFileSync(path.join(ROOT, "content", "ingredient-functions.json"), "utf8")
    );
    const allProducts = {};
    catalog.products.forEach((p) => {
      allProducts[p.handle] = buildProduct(p.handle);
    });
    pageGlobals = {
      template: { name: "page", suffix: "ingredients" },
      all_products: allProducts,
      shop: Object.assign({}, globals.shop, {
        metafields: {
          nexo: { ingredient_functions: { value: functionsDoc.functions } }
        }
      })
    };
  }

  let contentForLayout = "";
  for (const id of tpl.order) {
    const file = path.join(THEME, "sections", tpl.sections[id].type + ".liquid");
    const html = await engine.render(
      engine.parse(fs.readFileSync(file, "utf8")),
      pageGlobals
    );
    contentForLayout += html + "\n";
  }

  const layoutSrc = fs
    .readFileSync(path.join(THEME, "layout", "theme.liquid"), "utf8")
    /* liquidjs chokes on the Shopify '?' suffix */
    .replace(/posted_successfully\?/g, "posted_successfully");

  let out = await engine.render(
    engine.parse(layoutSrc),
    Object.assign({}, pageGlobals, { content_for_layout: contentForLayout })
  );

  if (mode === "product") {
    fs.writeFileSync(path.join(__dirname, "product.html"), out);
    console.log(`preview/product.html written (${handle}, ${localeName})`);
    return;
  }

  if (mode === "ingredients") {
    fs.writeFileSync(path.join(__dirname, "ingredients.html"), out);
    console.log(`preview/ingredients.html written (${localeName})`);
    return;
  }

  if (mode === "brand") {
    fs.writeFileSync(path.join(__dirname, "brand.html"), out);
    console.log(`preview/brand.html written (${localeName})`);
    return;
  }

  if (mode === "journal" || mode === "article") {
    fs.writeFileSync(path.join(__dirname, mode + ".html"), out);
    console.log(`preview/${mode}.html written (${localeName})`);
    return;
  }

  /* asset references inside section html also need the relative path */
  fs.writeFileSync(path.join(__dirname, "index.html"), out);

  /* static variant — approximates prefers-reduced-motion / no-JS:
     the ritual engine never loads, so .ritual--static stays in charge */
  const staticOut = out.replace(
    /<script src="\.\.\/theme\/assets\/nexo-ritual\.js" defer><\/script>/,
    ""
  );
  fs.writeFileSync(path.join(__dirname, "static.html"), staticOut);

  console.log(`preview/index.html + preview/static.html written (${localeName})`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
