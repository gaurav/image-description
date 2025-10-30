from pathlib import Path
import logging
import ollama

def describe_image(image_path: Path, model: str, temperature: float = 0.2):
    # Load all image metadata.
    image_metadata = "Filename: " + str(image_path).replace('_', ' ')
    image_metadata_filename = image_path.with_suffix('.txt')

    if image_metadata_filename.exists():
        with open(image_metadata_filename, 'r') as f:
            content = f.read()
        logging.info(f"Loading image-specific metadata from {image_metadata_filename}: \"{content}\"")
        image_metadata += "\n" + content + "\n"


    for parent in image_path.parents:
        metadata_filename = parent / "metadata.txt"
        if metadata_filename.exists():
            with open(metadata_filename, 'r') as f:
                content = f.read()
            logging.info(f"Loading parent metadata from {metadata_filename}: \"{content}\"")
            image_metadata += "\n" + content  + "\n"

    if image_metadata_filename.exists():
        with open(image_metadata_filename, 'r') as f:
            image_metadata += "\n" + f.read() + "\n"
            logging.info(f"Loading image metadata from {image_metadata_filename}")

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
        ],
        format={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Description and Entities Schema",
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "A short text describing the context or content."
                },
                "entities": {
                    "type": "array",
                    "description": "A list of entity identifiers or names referenced in the description.",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["description", "entities"],
            "additionalProperties": False
        },
        options={'temperature': float(temperature)},
    )

    return res['message']['content']