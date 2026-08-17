// La landing lee `catalog.json`, una vista generada desde catalog/plugins.yaml.
// GitHub Pages sirve archivos estáticos y no expone la API del panel, así que
// depender de /api/plugins dejaba la página publicada vacía. Cuando el panel
// local sí está levantado, su API se usa como fuente preferente.

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, function (character) {
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[character];
  });
}

function fromApi(data) {
  return {
    repository_version: data.repository_version,
    totals: null,
    plugins: data.plugins.map(function (item) {
      return {
        id: item.id,
        icon: item.icon,
        name: item.name,
        description: item.description,
        risk: item.risk,
        agents: item.components.agents,
        approval_required: item.policy.approval_required
      };
    })
  };
}

async function loadData() {
  try {
    const live = await fetch("/api/plugins", {cache: "no-store"});
    if (live.ok) {
      return fromApi(await live.json());
    }
  } catch (error) {
    // Sin panel local: se cae a la vista estática, que es el caso de Pages.
  }
  const response = await fetch("./catalog.json", {cache: "no-store"});
  if (!response.ok) {
    throw new Error("No se pudo leer catalog.json");
  }
  return response.json();
}

function render(data) {
  const plugins = data.plugins;
  const agents = new Set(plugins.flatMap(function (item) { return item.agents; }));
  const totals = data.totals || {
    plugins: plugins.length,
    agents: agents.size,
    evals: plugins.length * 4
  };
  const stats = [
    ["Plugins", totals.plugins],
    ["Agentes", totals.agents],
    ["Evaluaciones", totals.evals],
    ["Versión", data.repository_version]
  ];
  document.querySelector("#stats").innerHTML = stats.map(function (entry) {
    return '<article class="stat"><strong>' + escapeHtml(entry[1]) +
      '</strong><div>' + escapeHtml(entry[0]) + '</div></article>';
  }).join("");
  document.querySelector("#plugins").innerHTML = plugins.map(function (item) {
    const pills = item.agents.map(function (agent) {
      return '<span class="pill">' + escapeHtml(agent) + '</span>';
    }).join("");
    return '<article class="card"><h3>' + escapeHtml(item.icon) + ' ' +
      escapeHtml(item.name) + '</h3><p>' + escapeHtml(item.description) +
      '</p><p class="risk-' + escapeHtml(item.risk) + '">Riesgo: ' +
      escapeHtml(item.risk) + '</p><p class="gates">Aprobación humana: ' +
      escapeHtml((item.approval_required || []).join(", ")) + '</p>' +
      pills + '</article>';
  }).join("");
}

loadData().then(render).catch(function (error) {
  document.querySelector("#plugins").textContent = error.message;
});

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js").catch(function () {});
}
