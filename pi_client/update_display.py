import time
import requests
from PIL import Image
from io import BytesIO
from inky.auto import auto

# URL to your raw GitHub image (Updated to your repository)
IMAGE_URL = "https://raw.githubusercontent.com/PrymeTyme/the-daily-ink/main/newspaper.png"

def main():
    try:
        # 1. Automatically detect the connected Inky display
        display = auto()

        # 2. Download the image from GitHub (with a cache-busting timestamp parameter)
        print("Downloading the latest newspaper layout from GitHub...")
        response = requests.get(f"{IMAGE_URL}?t={int(time.time())}", timeout=30)
        response.raise_for_status()

        # 3. Load the image into PIL (Python Imaging Library)
        img = Image.open(BytesIO(response.content))

        # 4. Check dimensions and rotate if it's in portrait mode (480x800)
        if img.size == (480, 800):
            print("Portrait layout detected! Rotating image by 90 degrees...")
            # Rotate the image 90 degrees so the Inky display can process it natively
            img = img.rotate(90, expand=True)

        # Resize if the dimensions still don't match the display's native resolution
        if img.size != display.resolution:
            print(f"Resizing image: {img.size} -> {display.resolution}")
            img = img.resize(display.resolution, Image.Resampling.LANCZOS)

        # 5. Push the image to the E-Ink display
        print("Updating the Inky display (this may take up to a minute)...")
        display.set_image(img)
        display.show()
        print("Update completed successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Network error - Could not reach GitHub: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()