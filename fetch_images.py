from duckduckgo_search import DDGS
import os
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from urllib.parse import urlparse

# -------- CONFIG --------
IMAGE_FOLDER = "news_images"
MAX_RESULTS_PER_QUERY = 20
NUM_IMAGES_PER_HEADLINE = 2
MIN_WIDTH = 400
MIN_HEIGHT = 300
# ------------------------

def is_valid_image_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and any(ext in parsed.path.lower() for ext in [".jpg", ".jpeg", ".png"])

def is_valid_image(content):
    try:
        img = Image.open(BytesIO(content))
        img.verify()
        img = Image.open(BytesIO(content))  # reopen for dimension check
        return img.size[0] >= MIN_WIDTH and img.size[1] >= MIN_HEIGHT
    except (UnidentifiedImageError, OSError):
        return False

# ✅ NEW: For pipelined usage — per headline
def fetch_single_image_pair(headline, index, download_path=IMAGE_FOLDER):
    os.makedirs(download_path, exist_ok=True)
    clean_query = headline.strip().replace("Headline", "").strip(":")
    print(f"\n🔍 Searching images for Headline {index}: {clean_query}")

    img_paths = []
    with DDGS() as ddgs:
        try:
            results = ddgs.images(clean_query, max_results=MAX_RESULTS_PER_QUERY)
            saved = 0

            for result in results:
                if saved >= NUM_IMAGES_PER_HEADLINE:
                    break

                img_url = result.get("image")
                if not is_valid_image_url(img_url):
                    continue

                try:
                    response = requests.get(img_url, timeout=10)
                    content = response.content

                    if not is_valid_image(content):
                        continue

                    filename = f"img{index}_{saved+1}.jpg"
                    full_path = os.path.join(download_path, filename)
                    with open(full_path, "wb") as f:
                        f.write(content)

                    print(f"✅ Saved: {filename}")
                    img_paths.append(full_path)
                    saved += 1

                except Exception as e:
                    print(f"⚠️ Download error: {e}")

            if len(img_paths) < 2:
                print("❌ Not enough usable images found.")
                while len(img_paths) < 2:
                    img_paths.append(img_paths[-1] if img_paths else "static/default.jpg")  # fallback

        except Exception as e:
            print(f"❌ DuckDuckGo failed for '{clean_query}': {e}")
            img_paths = ["static/default.jpg", "static/default.jpg"]

    return img_paths[0], img_paths[1]

# 🔁 Original batch download method
def fetch_images(queries, download_path=IMAGE_FOLDER, num_images=NUM_IMAGES_PER_HEADLINE):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    else:
        for file in os.listdir(download_path):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                os.remove(os.path.join(download_path, file))

    with DDGS() as ddgs:
        for i, query in enumerate(queries):
            clean_query = query.strip().replace("Headline", "").strip(":")
            print(f"\n🔍 Searching images for: {clean_query}")

            try:
                results = ddgs.images(clean_query, max_results=MAX_RESULTS_PER_QUERY)
                saved = 0

                for result in results:
                    if saved >= num_images:
                        break

                    img_url = result.get("image")
                    if not is_valid_image_url(img_url):
                        continue

                    try:
                        response = requests.get(img_url, timeout=10)
                        content = response.content

                        if not is_valid_image(content):
                            continue

                        filename = f"img{i+1}_{saved+1}.jpg"
                        with open(os.path.join(download_path, filename), "wb") as f:
                            f.write(content)
                        print(f"✅ Saved: {filename}")
                        saved += 1

                    except Exception as e:
                        print(f"⚠️ Failed download: {e}")

                if saved == 0:
                    print("❌ No usable images found.")

            except Exception as e:
                print(f"❌ DuckDuckGo failed for '{clean_query}': {e}")

# 🧪 Test run
if __name__ == "__main__":
    from fetch_headlines import fetch_headlines
    fetch_images(fetch_headlines())
