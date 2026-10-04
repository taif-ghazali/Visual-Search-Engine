import os
import requests
from image_downloader import download_matches

class WebImageSearch:

    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")

        if not self.api_key:
            raise ValueError("SERPAPI_KEY is not set.")

    def upload_image(self, image_path):
        with open(image_path, "rb") as image_file: ## read binary (rb) mode
            response = requests.post(
                "https://serpapi.com/image",
                files={"image": image_file},
                data={"api_key": self.api_key}
            )

        response.raise_for_status()
        return response.json()

    def search_by_image(self, image_id):
        params = {
            "engine": "google_lens",
            "image_id": image_id,
            "type": "visual_matches",
            "api_key": self.api_key
        }

        response = requests.get(
            "https://serpapi.com/search",
            params=params
        )

        response.raise_for_status()
        return response.json()

    def get_visual_matches(self, results): 
        matches= results.get("visual_matches", [])
        clean_matches= []

        for match in matches:
            clean_matches.append({
                "title": match.get("title"),
                "link": match.get("link"), 
                "image": match.get("image"), 
                "thumbnail": match.get("thumbnail"), 
                "source": match.get("source")
            })

        return clean_matches

    # def search(self, query):
    #     params = {
    #         "engine": "google_images",
    #         "q": query,
    #         "api_key": self.api_key
    #     }

    #     response = requests.get(
    #         "https://serpapi.com/search",
    #         params=params
    #     )

    #     response.raise_for_status()

    #     return response.json()


if __name__ == "__main__":

    search = WebImageSearch()

    # SerpApi supports uploading a local JPG/PNG/WebP directly. The upload limit is 500 KB, 
    # and the resulting image_id lasts 10 minutes. Google Lens can then return structured visual_matches, 
    # including the actual image URL, thumbnail, source page, title, etc

    
    for query_index in range(6):
        image_path = f"examples/query/query{query_index}.jpg"
        print(f"\n======QUERY {query_index}======")

        upload_result= search.upload_image(image_path)
        image_id = upload_result["image_id"]

        print("Image Uploaded")
        print("Image ID:", image_id)

        results= search.search_by_image(image_id)
        visual_matches= search.get_visual_matches(results)
        print("Visual matches returned:", len(visual_matches))

        download_matches(visual_matches, query_index)

    # image_path = "examples/query/query.jpg"
    # upload_result= search.upload_image(image_path)
    # image_id = upload_result["image_id"]

    # print("Image Uploaded")
    # print("Image ID:", image_id)
    
    # results = search.search_by_image(image_id)
    # visual_matches= search.get_visual_matches(results)

    # print("Response keys:", results.keys())
    # download_matches(visual_matches, 0)

    # first_match = visual_matches[0]
    # image_url = first_match["image"]

    # download_image(
    #     image_url,
    #     "examples/candidates/test_image.jpg"
    # )

    # print("First candidate downloaded successfully!")
    # print("Google Lens Search Successful!!")
    # print("Keys:", results.keys())

    # if "visual_matches" in results:
    #     print("Visual matches returned:", len(visual_matches))
    # else:
    #     print("⚠️ visual_matches field missing!")
    #     print("Full response:", results)

    # print("\n5 CLEAN MATCHES:")
    # print(visual_matches[0:5])