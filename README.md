# Local semantic image search using Openai CLIP

## Download Model

Before running the application, download the **ViT-B-32.pt** model:

https://openaipublic.azureedge.net/clip/models/40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af/ViT-B-32.pt

Place the downloaded `ViT-B-32.pt` file in the **project root folder**.


A web-based image search application powered by **OpenAI CLIP**. The project uses image embeddings to find visually similar images and provides a simple web interface for searching and exploring image collections.

## ✨ Features

* 🔎 Search images using text queries
* 🖼️ Find visually similar images using CLIP embeddings
* ⚡ Fast embedding-based image retrieval
* 🌐 Web interface built with FastAPI
* 📊 Pre-generated image embeddings for faster searches
* 🐍 Python-based backend

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **PyTorch**
* **OpenAI CLIP**
* **NumPy**
* **Pillow**
* **TorchVision**
* **HTML / CSS / JavaScript**

## 📁 Project Structure

```text
openclip/
├── photos/                 # Image collection
├── static/                 # Static web assets
├── templates/              # HTML templates
├── main.py                 # Core application
├── web_app.py              # Web application
├── photo_embeddings.npy    # Image embeddings
├── photo_files.json        # Image metadata
├── requirements-web.txt    # Python dependencies
├── run_web.bat             # Windows launcher
└── README.md
```

> The `photos` directory is included in the repository structure, but the actual images are not committed to GitHub.

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/openclip-web-app.git
cd openclip-web-app
```

Install the dependencies:

```bash
pip install -r requirements-web.txt
```

## ▶️ Running the Application

On Windows, you can run:

```bash
run_web.bat
```

Or start the application manually:

```bash
python web_app.py
```

Then open the local URL shown by the application in your browser.

## 🧠 How It Works

The application uses CLIP to convert images and text into embeddings in a shared vector space.

```text
Text Query
    ↓
CLIP Text Encoder
    ↓
Text Embedding
    ↓
Compare with Image Embeddings
    ↓
Rank Similar Images
    ↓
Display Results
```

## 📌 Notes

The pre-trained CLIP model file is intentionally excluded from the Git repository because of its large size.

The `photos/` directory is kept in the repository using a `.gitkeep` file so the folder structure is preserved without uploading the image collection.

## 📄 License

This project is for educational and development purposes.
