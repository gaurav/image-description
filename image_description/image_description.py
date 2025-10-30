from pathlib import Path
import logging
import ollama

def describe_image(image_path: Path, model: str):
    # Load image metadata.
    image_metadata = ""
    image_metadata_filename = image_path.with_suffix('.txt')
    logging.info(f"Loading image metadata from {image_metadata_filename}")
    if image_metadata_filename.exists():
        with open(image_metadata_filename, 'r') as f:
            image_metadata = f.read()

    # Query model
    logging.debug(f"Querying model {model} for image {image_path} with metadata: {image_metadata}")
    res = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Given the following metadata, describe this image: {image_metadata}",
                "images": [str(image_path)]
            }
        ]
    )

    return res['message']['content']