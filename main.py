import os
import json
import torch
import clip
import numpy as np
from PIL import Image


# ============================================================
# CONFIGURATION
# ============================================================

# Change this if your photos folder is somewhere else
PHOTOS_DIR = "./photos"

# Your existing OpenAI CLIP model
MODEL_PATH = "./ViT-B-32.pt"

# Files created by this program
EMBEDDINGS_FILE = "photo_embeddings.npy"
PHOTOS_FILE = "photo_files.json"

# Number of results to show
TOP_K = 10


# ============================================================
# LOAD CLIP
# ============================================================

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading OpenAI CLIP ViT-B/32...")
print("Device:", device)

model, preprocess = clip.load(
    MODEL_PATH,
    device=device
)

model.eval()

print("CLIP loaded.")


# ============================================================
# FIND PHOTOS
# ============================================================

def get_photos():

    photos = []

    for root, dirs, files in os.walk(PHOTOS_DIR):

        for filename in files:

            if filename.lower().endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp",
                    ".bmp",
                    ".gif"
                )
            ):

                path = os.path.join(root, filename)

                photos.append(path)

    return sorted(photos)


# ============================================================
# CREATE PHOTO EMBEDDINGS
# ============================================================

def create_index():

    photos = get_photos()

    print()
    print("Photos found:", len(photos))
    print()

    embeddings = []
    valid_photos = []

    with torch.no_grad():

        for i, photo_path in enumerate(photos):

            try:

                print(
                    f"[{i + 1}/{len(photos)}] "
                    f"{photo_path}"
                )

                # Open image
                image = Image.open(
                    photo_path
                ).convert("RGB")

                # Prepare image for CLIP
                image_input = preprocess(
                    image
                ).unsqueeze(0).to(device)

                # Image -> embedding
                image_features = model.encode_image(
                    image_input
                )

                # Normalize
                image_features = (
                    image_features /
                    image_features.norm(
                        dim=-1,
                        keepdim=True
                    )
                )

                embeddings.append(
                    image_features.cpu().numpy()[0]
                )

                valid_photos.append(
                    photo_path
                )

            except Exception as e:

                print(
                    "ERROR:",
                    photo_path,
                    e
                )

    # Convert to numpy array
    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    # Save embeddings
    np.save(
        EMBEDDINGS_FILE,
        embeddings
    )

    # Save corresponding filenames
    with open(
        PHOTOS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            valid_photos,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("================================")
    print("INDEX CREATED")
    print("Photos:", len(valid_photos))
    print("Embedding size:", embeddings.shape)
    print("================================")
    print()


# ============================================================
# SEARCH
# ============================================================

def search_photos(query, top_k=TOP_K):

    # Load embeddings
    image_embeddings = np.load(
        EMBEDDINGS_FILE
    )

    # Load photo filenames
    with open(
        PHOTOS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        photos = json.load(f)

    # Convert search text into tokens
    text = clip.tokenize(
        [query]
    ).to(device)

    with torch.no_grad():

        # Text -> embedding
        text_features = model.encode_text(
            text
        )

        # Normalize
        text_features = (
            text_features /
            text_features.norm(
                dim=-1,
                keepdim=True
            )
        )

    # Move to CPU
    text_features = (
        text_features
        .cpu()
        .numpy()[0]
    )

    # Compare text with every image
    scores = image_embeddings @ text_features

    # Sort highest score first
    indices = np.argsort(scores)[::-1]

    # Limit number of results
    indices = indices[:top_k]

    results = []

    for index in indices:

        results.append(
            (
                photos[index],
                float(scores[index])
            )
        )

    return results


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    # --------------------------------------------------------
    # Create index if it doesn't exist
    # --------------------------------------------------------

    if not os.path.exists(
        EMBEDDINGS_FILE
    ) or not os.path.exists(
        PHOTOS_FILE
    ):

        print()
        print("No photo index found.")
        print("Creating index...")
        print()

        create_index()

    else:

        print()
        print("Existing photo index found.")
        print()


    # --------------------------------------------------------
    # Search loop
    # --------------------------------------------------------

    print("========================================")
    print("       SEMANTIC PHOTO SEARCH")
    print("========================================")
    print()
    print("Examples:")
    print("  dog")
    print("  dog playing outside")
    print("  people at a birthday party")
    print("  sunset at the beach")
    print("  red car")
    print("  food on a table")
    print()
    print("Type 'exit' to quit.")
    print()


    while True:

        query = input("Search: ").strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        results = search_photos(
            query,
            TOP_K
        )

        print()
        print(
            f"Top {len(results)} matches "
            f"for: {query}"
        )

        print("----------------------------------------")

        for rank, (path, score) in enumerate(
            results,
            start=1
        ):

            print(
                f"{rank:2d}. "
                f"{score:.4f}  "
                f"{path}"
            )

        print()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()

