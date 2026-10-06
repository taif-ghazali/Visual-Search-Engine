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

def download_matches(matches, target_dir, target_count= 8):
    download_paths = []
    successful = 0 
    failed = 0

    target_dir.mkdir(parents= True, exist_ok= True)

    for match in matches:
        image_url = match["image"]

        image_number = successful
        save_path = target_dir/f"candidate_{image_number: 02d}.jpg"

        # image_number = start_index*10 + successfull
        # save_path = f"examples/candidates/test_image{image_number:02d}.jpg"

        try:
            download_image(image_url, save_path)
            print(f"Downloaded: {save_path}")
            successful += 1
            download_paths.append(save_path)
            if (successful == target_count):
                break

        except (requests.exceptions.RequestException, ValueError, UnidentifiedImageError) as e:
            print(f"Failed: candidate_{image_number:02d}.jpg")
            print(f"Reason: {e}")
            failed +=1

    print(f"Downloaded {successful} images")
    print(f"Failed to download {failed} images")
    return download_paths
# if __name__ == "__main__":
#     image_url = "PASTE_IMAGE_URL_HERE"

#     download_image(
#         image_url,
#         "test_image.jpg"
#     )

#     print("Image downloaded successfully!")