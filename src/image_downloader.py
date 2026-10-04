import requests

def download_image(image_url, save_path):
    response = requests.get(image_url)
    response.raise_for_status()

    with open(save_path, "wb") as f: ## write binary
        f.write(response.content)

def download_matches(matches, start_index):
    successfull = 0 
    failed = 0

    for i, match in enumerate(matches[:10]):
        image_url = match["image"]
        image_number = start_index*10 + i

        save_path = f"examples/candidates/test_image{image_number:02d}.jpg"

        try:
            download_image(image_url, save_path)
            print(f"Downloaded: {save_path}")
            successfull += 1

        except requests.exceptions.RequestException as e:
            print(f"Failed: test_image{image_number:02d}.jpg")
            print(f"Reason: {e}")
            failed +=1

    print(f"Downloaded {successfull}/10 images")
    print(f"Failed to download {failed} images")
# if __name__ == "__main__":
#     image_url = "PASTE_IMAGE_URL_HERE"

#     download_image(
#         image_url,
#         "test_image.jpg"
#     )

#     print("Image downloaded successfully!")