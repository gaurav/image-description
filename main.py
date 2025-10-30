import json
import logging
import os
from pathlib import Path

import click

from image_description import image_description

logging.basicConfig(level=logging.INFO)

IMAGE_EXTENSIONS_LC = (
    '.jpg',
    '.jpeg'
)


@click.command()
@click.argument("IMAGE_PATHS", default=["./images"], nargs=-1, type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.option("--model", default="gemma3", help="Model to use for image description")
@click.option("--temperature", default="0.2", help="Temperature for the LLM model")
def main(image_paths, model, temperature):
    """
    Processes the given directory or file path to find images, logs their discovery, and generates descriptions
    based on the provided model.

    The function traverses through the provided path, identifying files with supported image extensions.
    For each valid image, a description is generated using the specified model. All progress and descriptive
    results are logged.

    \f

    :param image_path: Path to the image file or folder containing images to process
    :type image_path: str
    :param model: Name of the model used to generate image descriptions
    :type model: str
    :return: None
    """
    logging.info(f"Processing images from {image_paths} with model {model}")

    for image_path in image_paths:
        for root, dirs, files in os.walk(click.format_filename(image_path)):
            for filename in files:
                filepath = os.path.join(root, filename)
                logging.debug(f"Checking image: {filepath}")
                if filepath.endswith(IMAGE_EXTENSIONS_LC):
                    logging.info(f"Found image: {filepath}")
                    description = image_description.describe_image(Path(filepath), model, temperature)
                    logging.info(f" - Image description: {json.dumps(description, indent=2)}")
                    with open(Path(filepath).with_suffix('.json'), "w") as f:
                        json.dump(description, f)

if __name__ == "__main__":
    main()
