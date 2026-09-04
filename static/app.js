const gallery = document.querySelector("#gallery");
const queryInput = document.querySelector("#query");
const searchForm = document.querySelector("#searchForm");
const clearBtn = document.querySelector("#clearBtn");
const embedBtn = document.querySelector("#embedBtn");
const statusEl = document.querySelector("#status");
const resultCount = document.querySelector("#resultCount");
const resultsTitle = document.querySelector("#resultsTitle");
const indexStatus = document.querySelector("#indexStatus");
const embedMessage = document.querySelector("#embedMessage");

const lightbox = document.querySelector("#lightbox");
const lightboxImage = document.querySelector("#lightboxImage");
const lightboxCaption = document.querySelector("#lightboxCaption");
const closeLightbox = document.querySelector("#closeLightbox");

function filename(path) {
  return path.split(/[\\/]/).pop();
}

function renderPhotos(items) {
  gallery.replaceChildren();

  if (!items.length) {
    const empty = document.createElement("p");
    empty.textContent = "No images found.";
    gallery.appendChild(empty);
    return;
  }

  for (const item of items) {
    const card = document.createElement("article");
    card.className = "card";

    const button = document.createElement("button");
    button.type = "button";
    button.setAttribute("aria-label", `Open ${filename(item.path)}`);

    const img = document.createElement("img");
    img.src = item.url;
    img.alt = filename(item.path);
    img.loading = "lazy";
    img.decoding = "async";

    const meta = document.createElement("div");
    meta.className = "card-meta";
    meta.textContent = item.score == null
      ? filename(item.path)
      : `${filename(item.path)}  ·  ${(item.score * 100).toFixed(1)}%`;

    button.append(img, meta);
    button.addEventListener("click", () => {
      lightboxImage.src = item.url;
      lightboxImage.alt = filename(item.path);
      lightboxCaption.textContent = filename(item.path);
      lightbox.showModal();
    });

    card.appendChild(button);
    gallery.appendChild(card);
  }
}

async function loadAll() {
  statusEl.textContent = "Loading photos…";
  const response = await fetch("/api/photos");
  const data = await response.json();

  resultsTitle.textContent = "All photos";
  resultCount.textContent = `${data.count} PHOTOS`;
  indexStatus.textContent = `${data.count} PHOTOS FOUND`;
  renderPhotos(data.photos);
  statusEl.textContent = "";
}

async function search(query) {
  statusEl.textContent = `Searching “${query}”…`;
  const response = await fetch("/api/search", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({query, top_k: 24})
  });

  const data = await response.json();

  if (!response.ok) {
    statusEl.textContent = data.detail || "Search failed.";
    return;
  }

  resultsTitle.textContent = `Matches for “${data.query}”`;
  resultCount.textContent = `${data.count} RESULTS`;
  renderPhotos(data.photos);
  statusEl.textContent = "";
}

searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = queryInput.value.trim();

  if (!query) {
    await loadAll();
    return;
  }

  await search(query);
});

clearBtn.addEventListener("click", async () => {
  queryInput.value = "";
  await loadAll();
});

embedBtn.addEventListener("click", async () => {
  embedBtn.disabled = true;
  embedBtn.querySelector("span:first-child").textContent = "Embedding…";
  embedMessage.textContent = "OpenCLIP is processing the photos. Keep this page open.";

  try {
    const response = await fetch("/api/embed", {method: "POST"});
    const data = await response.json();

    if (!response.ok) throw new Error(data.detail || "Embedding failed.");

    embedMessage.textContent = data.message;
    indexStatus.textContent = `${data.count} PHOTOS INDEXED`;
    await loadAll();
  } catch (error) {
    embedMessage.textContent = error.message;
  } finally {
    embedBtn.disabled = false;
    embedBtn.querySelector("span:first-child").textContent = "Embed photos";
  }
});

closeLightbox.addEventListener("click", () => lightbox.close());

lightbox.addEventListener("click", (event) => {
  if (event.target === lightbox) lightbox.close();
});

loadAll().catch(() => {
  statusEl.textContent = "Could not connect to the local server.";
});
