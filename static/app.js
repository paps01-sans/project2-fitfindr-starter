let currentResults = [];
let latestSession = null;

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
      body: JSON.stringify({ query })
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
