async function search() {
  let query = document.getElementById("queryInput").value;

  let res = await fetch("http://127.0.0.1:8000/query", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      query: query,
    }),
  });

  let data = await res.json();

  let output = "";

  output += "<h3>Query:</h3>" + data.query;

  output += "<br><b>Cache Hit:</b> " + data.cache_hit;

  output += "<br><b>Cluster:</b> " + data.dominant_cluster;

  output += "<hr>";

  output += data.result.replaceAll("\n", "<br>");

  document.getElementById("results").innerHTML = output;
}

async function getStats() {
  let res = await fetch("http://127.0.0.1:8000/cache/stats");

  let data = await res.json();

  alert(JSON.stringify(data, null, 2));
}

async function clearCache() {
  await fetch("http://127.0.0.1:8000/cache", {
    method: "DELETE",
  });

  alert("Cache cleared");
}
