import logging
import os
from pathlib import Path

from image_description import image_description

logging.basicConfig(level=logging.INFO)

IMAGE_EXTENSIONS_LC = (
    '.jpg',
    '.jpeg'
)

def main(image_path="./images", model="llava"):
    for root, dirs, files in os.walk(image_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            logging.debug(f"Checking image: {filepath}")
            if filepath.endswith(IMAGE_EXTENSIONS_LC):
                logging.info(f"Found image: {filepath}")
                description = image_description.describe_image(Path(filepath), model)
                logging.info(f" - Image description: {description}")

if __name__ == "__main__":
    main()
