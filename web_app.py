import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import main

BASE_DIR = Path(__file__).resolve().parent
PHOTOS_DIR = BASE_DIR / "photos"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="OpenCLIP Photo Search")

# Serve the existing photo folder without moving your current dataset.
app.mount("/photos", StaticFiles(directory=str(PHOTOS_DIR)), name="photos")
# Serve CSS and JavaScript
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


class SearchRequest(BaseModel):
    query: str
    top_k: int = 24


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "templates" / "index.html")


def web_photo_url(path: str) -> str:
    # main.py stores paths such as ./photos/example.jpg.
    relative = Path(path).resolve().relative_to(PHOTOS_DIR.resolve())
    return "/photos/" + relative.as_posix()


@app.get("/api/photos")
def all_photos():
    photos = main.get_photos()
    return {
        "count": len(photos),
        "photos": [{"path": p, "url": web_photo_url(p)} for p in photos],
    }


@app.post("/api/search")
def search(request: SearchRequest):
    query = request.query.strip()
    if not query:
        return all_photos()

    if not os.path.exists(main.EMBEDDINGS_FILE) or not os.path.exists(main.PHOTOS_FILE):
        raise HTTPException(
            status_code=409,
            detail="No embedding index exists yet. Click 'Embed photos' first.",
        )

    top_k = max(1, min(request.top_k, 100))
    results = main.search_photos(query, top_k)

    return {
        "query": query,
        "count": len(results),
        "photos": [
            {
                "path": path,
                "url": web_photo_url(path),
                "score": score,
            }
            for path, score in results
        ],
    }


@app.post("/api/embed")
def embed():
    try:
        main.create_index()
        photos = main.get_photos()
        return {
            "status": "success",
            "count": len(photos),
            "message": f"Embedded {len(photos)} photos successfully.",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
