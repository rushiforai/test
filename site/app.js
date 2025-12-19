fetch("../data/posts.json")
  .then(r => r.json())
  .then(posts => {
    const feed = document.getElementById("feed");

    posts.forEach(p => {
      const row = document.createElement("div");
      row.className = "row";
      row.innerHTML = `
        <strong>${p.code}</strong>
        <span>${p.platform}</span>
        <a href="${p.url}" target="_blank">source</a>
        <span>${new Date(p.timestamp).toLocaleString()}</span>
      `;
      feed.appendChild(row);
    });
  });
