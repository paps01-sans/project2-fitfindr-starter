let currentResults = [];
let latestSession = null;

const wardrobeKey = "fitfindr-wardrobe";
const exampleWardrobe = {
  items: [
    { id: "w_ui_001", name: "White ribbed tank top", category: "tops", colors: ["white"], style_tags: ["minimal", "basics"], notes: "Goes with everything" },
    { id: "w_ui_002", name: "Dark wash jeans", category: "bottoms", colors: ["dark blue", "indigo"], style_tags: ["denim", "streetwear"], notes: null },
    { id: "w_ui_003", name: "Chunky white sneakers", category: "shoes", colors: ["white"], style_tags: ["sneakers", "chunky", "streetwear"], notes: null }
  ]
};

let wardrobe = loadJson(wardrobeKey, exampleWardrobe);

function loadJson(key, fallback) {
  try {
    const value = JSON.parse(localStorage.getItem(key));
    return value ?? fallback;
  } catch {
    return fallback;
  }
}

function saveJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function composeQuery() {
  const pieces = [document.querySelector("#query").value.trim()];
  const size = document.querySelector("#size").value.trim();
  const budget = document.querySelector("#budget").value.trim();
  if (size) pieces.push(`size ${size}`);
  if (budget) pieces.push(`under $${budget}`);
  return pieces.join(" ");
}

function setStatus(message, kind = "") {
  const status = document.querySelector("#status");
  status.textContent = message;
  status.className = `status ${kind}`;
}

document.querySelector("#search-form").addEventListener("submit", async event => {
  event.preventDefault();
  const button = document.querySelector("#search-button");
  const query = composeQuery();
  button.disabled = true;
  setStatus("Searching and building your fit…", "loading");

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, wardrobe })
    });
    const session = await response.json();
    latestSession = session;

    if (!response.ok) {
      setStatus(session.error || "The request could not be completed.", "error");
      return;
    }

    if (session.error && !session.selected_item) {
      setStatus(session.error, "error");
      document.querySelector("#recommendation").hidden = true;
      document.querySelector("#results-section").hidden = true;
      return;
    }

    if (session.error) setStatus(session.error, "error");
    else setStatus(`${session.search_results.length} matching listings found.`);
    renderSession(session);
  } catch (error) {
    setStatus(`Could not reach FitFindr. ${error.message}`, "error");
  } finally {
    button.disabled = false;
  }
});

function renderSession(session) {
  const item = session.selected_item;
  const comparison = session.price_comparison;
  const recommendation = document.querySelector("#recommendation");
  recommendation.hidden = false;
  recommendation.innerHTML = `
    <div class="recommendation-grid">
      <article class="hero-item">
        <p class="eyebrow">Top recommendation</p>
        <h2>${escapeHtml(item.title)}</h2>
        <p><strong>$${item.price}</strong> · ${escapeHtml(item.platform)} · ${escapeHtml(item.size)}</p>
        <p>${escapeHtml(item.description)}</p>
      </article>
      <div class="detail-panel">
        <div class="detail-block">
          <h3>Outfit</h3>
          <p>${escapeHtml(session.outfit_suggestion || "Outfit unavailable.")}</p>
        </div>
        <div class="detail-block">
          <h3>Fit card</h3>
          <p>${escapeHtml(session.fit_card || "Fit card unavailable.")}</p>
        </div>
        ${comparison ? `
          <div class="detail-block">
            <h3>Price check</h3>
            ${comparison.status === "compared"
              ? `<p><strong>$${comparison.average_comparable_price}</strong> average · <span class="price-verdict">${escapeHtml(comparison.verdict)}</span> across ${comparison.comparable_count} listings</p>`
              : `<p>${escapeHtml(comparison.message)}</p>`}
          </div>` : ""}
      </div>
    </div>`;

  currentResults = session.search_results || [];
  document.querySelector("#results-section").hidden = false;
  document.querySelector("#category-filter").value = "";
  renderResults();
}

function renderResults() {
  const category = document.querySelector("#category-filter").value;
  const filtered = category
    ? currentResults.filter(item => item.category === category)
    : currentResults;

  document.querySelector("#results").innerHTML = filtered.map(item => {
    const selected = latestSession?.selected_item?.id === item.id;
    return `
      <article class="result-card ${selected ? "selected" : ""}">
        <p class="eyebrow">${escapeHtml(item.category)} · ${escapeHtml(item.condition)}</p>
        <h3>${escapeHtml(item.title)}</h3>
        <p class="price">$${item.price}</p>
        <p>${escapeHtml(item.brand || "Unknown brand")} · ${escapeHtml(item.size)}</p>
        <p>${escapeHtml(item.platform)} · ${escapeHtml((item.colors || []).join(", "))}</p>
      </article>`;
  }).join("") || "<p>No listings in this category.</p>";
}

document.querySelector("#category-filter").addEventListener("change", renderResults);

function splitList(value) {
  return value
    .split(",")
    .map(item => item.trim())
    .filter(Boolean);
}

const wardrobeDialog = document.querySelector("#wardrobe-dialog");

document.querySelector("#wardrobe-button").addEventListener("click", () => {
  renderWardrobe();
  wardrobeDialog.showModal();
});

document.querySelector("#close-wardrobe").addEventListener("click", () => {
  wardrobeDialog.close();
});

document.querySelector("#wardrobe-form").addEventListener("submit", event => {
  event.preventDefault();

  const id = document.querySelector("#item-id").value;
  const name = document.querySelector("#item-name").value.trim();
  const category = document.querySelector("#item-category").value;
  const colors = splitList(document.querySelector("#item-colors").value);
  const styleTags = splitList(document.querySelector("#item-tags").value);
  const notes = document.querySelector("#item-notes").value.trim() || null;

  if (!name || !colors.length) {
    setStatus("Add an item name and at least one color.", "error");
    return;
  }

  const allowedCategories = ["tops", "bottoms", "outerwear", "shoes", "accessories"];
  if (!allowedCategories.includes(category)) {
    setStatus("Choose a valid wardrobe category.", "error");
    return;
  }

  const item = {
    id: id || `w_ui_${Date.now()}`,
    name,
    category,
    colors,
    style_tags: styleTags,
    notes
  };

  const items = wardrobe.items || [];
  wardrobe = {
    items: id
      ? items.map(existing => existing.id === id ? item : existing)
      : [...items, item]
  };

  saveJson(wardrobeKey, wardrobe);
  event.currentTarget.reset();
  document.querySelector("#item-id").value = "";
  renderWardrobe();
  setStatus("Wardrobe saved.");
});

document.querySelector("#reset-wardrobe").addEventListener("click", () => {
  wardrobe = structuredClone(exampleWardrobe);
  saveJson(wardrobeKey, wardrobe);
  renderWardrobe();
  setStatus("Example wardrobe restored.");
});

function renderWardrobe() {
  const container = document.querySelector("#wardrobe-items");
  const items = wardrobe.items || [];

  container.innerHTML = items.map(item => `
    <div class="wardrobe-item">
      <div>
        <strong>${escapeHtml(item.name)}</strong>
        <span>${escapeHtml(item.category)} · ${escapeHtml((item.colors || []).join(", "))}</span>
      </div>
      <button class="small-button" type="button" data-edit="${escapeHtml(item.id)}">Edit</button>
      <button class="small-button" type="button" data-remove="${escapeHtml(item.id)}">Remove</button>
    </div>
  `).join("") || "<p>Your wardrobe is empty.</p>";

  container.querySelectorAll("[data-edit]").forEach(button => {
    button.addEventListener("click", () => {
      const item = items.find(candidate => candidate.id === button.dataset.edit);
      document.querySelector("#item-id").value = item.id;
      document.querySelector("#item-name").value = item.name;
      document.querySelector("#item-category").value = item.category;
      document.querySelector("#item-colors").value = (item.colors || []).join(", ");
      document.querySelector("#item-tags").value = (item.style_tags || []).join(", ");
      document.querySelector("#item-notes").value = item.notes || "";
    });
  });

  container.querySelectorAll("[data-remove]").forEach(button => {
    button.addEventListener("click", () => {
      wardrobe = {
        items: items.filter(item => item.id !== button.dataset.remove)
      };
      saveJson(wardrobeKey, wardrobe);
      renderWardrobe();
      setStatus("Wardrobe item removed.");
    });
  });
}
