import os
import requests

class WebImageSearch:

    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")

        if not self.api_key:
            raise ValueError("SERPAPI_KEY is not set.")

    def search(self, query, limit=6):

        params = {
            "engine": "google_images",
            "q": query,
            "api_key": self.api_key
        }

        response = requests.get(
            "https://serpapi.com/search",
            params=params
        )

        response.raise_for_status()

        results = response.json()

        images = results.get("images_results", [])

        return [
            {
                "title": image.get("title"),
                "thumbnail": image.get("thumbnail"),
                "original": image.get("original"),
                "source": image.get("source"),
                "link": image.get("link")
            }
            for image in images[:limit]
        ]