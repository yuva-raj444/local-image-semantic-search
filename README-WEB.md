# Web gallery add-on for the existing OpenCLIP project

This add-on keeps the original project structure and uses the existing:

- `main.py`
- `photos/`
- `photo_embeddings.npy`
- `photo_files.json`
- `ViT-B-32.pt`

## Add these files

```text
openclip/
├── main.py
├── photos/
├── photo_embeddings.npy
├── photo_files.json
├── ViT-B-32.pt
├── web_app.py
├── run_web.bat
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## Install

```bat
pip install -r requirements-web.txt
```

## Run

```bat
run_web.bat
```

Then open:

`http://127.0.0.1:8000`

The gallery shows every image in `photos/` by default.

A search such as `red car` or `dog playing outside` calls the existing `main.search_photos()` function and ranks images using the existing embedding index.

Click **Embed photos** after adding new images. It calls the existing `main.create_index()` function and regenerates `photo_embeddings.npy` and `photo_files.json`.
