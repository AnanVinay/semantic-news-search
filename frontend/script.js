async function search() {
  let query = document.getElementById("queryInput").value;

  if (query.trim() === "") {
    alert("Please enter a query.");
    return;
  }

  let res = await fetch("/query", {
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

  output += "<h3>Query:</h3> " + data.query;

  output += "<br><b>Cache Hit:</b> " + data.cache_hit;

  output += "<br><b>Dominant Cluster:</b> " + data.dominant_cluster;

  if (data.matched_query !== null) {
    output += "<br><b>Matched Cached Query:</b> " + data.matched_query;
  }

  if (data.similarity_score !== null) {
    output +=
      "<br><b>Similarity Score:</b> " +
      Number(data.similarity_score).toFixed(3);
  }

  output += "<hr>";

  output += "<h3>Search Results</h3>";

  let docs = data.result.split("---");

  docs.forEach((doc, index) => {
    output += "<div class='result-card'>";

    output += "<b>Document " + (index + 1) + "</b><br>";

    output += "<p>" + doc.trim() + "</p>";

    output += "</div>";
  });

  document.getElementById("results").innerHTML = output;
}

async function getStats() {
  let res = await fetch("/cache/stats");

  let data = await res.json();

  alert(
    "Cache Stats\n\n" +
      "Total Entries: " +
      data.total_entries +
      "\n" +
      "Hits: " +
      data.hit_count +
      "\n" +
      "Misses: " +
      data.miss_count +
      "\n" +
      "Hit Rate: " +
      data.hit_rate,
  );
}

async function clearCache() {
  await fetch("/cache", {
    method: "DELETE",
  });

  alert("Cache cleared");
}
