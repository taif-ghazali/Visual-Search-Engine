import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError

def download_image(image_url, save_path):
    response = requests.get(image_url)
    response.raise_for_status()

    image= Image.open(BytesIO(response.content))

    image = image.convert("RGB")
    image.save(save_path, format="JPEG", quality = 95)

    # with open(save_path, "wb") as f: ## write binary
    #     f.write(response.content)

def download_matches(matches, start_index, target_count= 8):
    download_paths = []
    successfull = 0 
    failed = 0

    for match in matches:
        image_url = match["image"]
        image_number = start_index*10 + successfull

        save_path = f"examples/candidates/test_image{image_number:02d}.jpg"

        try:
            download_image(image_url, save_path)
            print(f"Downloaded: {save_path}")
            successfull += 1
            download_paths.append(save_path)
            if (successfull == target_count):
                break

        except (requests.exceptions.RequestException, ValueError, UnidentifiedImageError) as e:
            print(f"Failed: test_image{image_number:02d}.jpg")
            print(f"Reason: {e}")
            failed +=1

    print(f"Downloaded {successfull} images")
    print(f"Failed to download {failed} images")
    return download_paths
# if __name__ == "__main__":
#     image_url = "PASTE_IMAGE_URL_HERE"

#     download_image(
#         image_url,
#         "test_image.jpg"
#     )

#     print("Image downloaded successfully!")