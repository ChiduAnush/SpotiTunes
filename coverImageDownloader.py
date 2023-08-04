# https://i.scdn.co/image/ab67616d0000b273ba5db46f4b838ef6027e6f96

import requests


def download_image(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
        print("Image downloaded successfully.")
    else:
        print("Failed to download image.")


# Example usage
url = "https://i.scdn.co/image/ab67616d0000b273ba5db46f4b838ef6027e6f96"
file_name = "image.jpg"
download_image(url, file_name)
