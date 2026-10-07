import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from web_image_search import WebImageSearch

search = WebImageSearch()
images = search.search("Ferrari 488", limit=6)

print(f"Found {len(images)} images")

for i, image in enumerate(images, start=1):
    print(f"\n{i}. {image['title']}")
    print(f"   Thumbnail: {image['thumbnail']}")
    print(f"   Original:  {image['original']}")