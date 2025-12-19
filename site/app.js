let posts = [];

fetch("../data/posts.json")
  .then(r => r.json())
  .then(data => {
    posts = data;
    render("all");
  });

function filter(platform) {
  render(platform);
}

function render(platform) {
  const feed = document.getElementById("feed");
  feed.innerHTML = "";

  posts
    .filter(p => platform === "all" || p.platform === platform)
    .forEach(p => {
      const div = document.createElement("div");
      div.className = "post";
      div.innerHTML = `
        <span class="platform">${p.platform}</span>
        <a href="${p.url}" target="_blank">${p.text}</a>
        <div class="meta">${new Date(p.timestamp).toLocaleString()}</div>
      `;
      feed.appendChild(div);
    });
}
