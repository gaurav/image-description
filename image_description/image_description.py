import json
from json import JSONDecodeError
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
    logging.info(f"Querying model {model} for image {image_path} with metadata: {image_metadata}")
    res = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Given the following metadata, describe this image, listing all the entities referenced or visible, and also listing any animal or plant individuals you can see and any interactions between them: {image_metadata}",
                "images": [str(image_path)]
            }
        ],
        format={
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "A short text describing the context or content."
                },
                "individuals": {
                    "type": "array",
                    "description": "A list of individuals in this image.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "A detailed description of the individual.",
                            },
                            "interactions": {
                                "type": "array",
                                "description": "A list of interactions that this individual is participating in as well as some information on which individual it is interacting with.",
                                "items": {
                                    "type": "string",
                                }
                            },
                        }
                    }
                },
                "entities": {
                    "type": "array",
                    "description": "A list of entities visible or referenced in this image.",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["description", "entities", "individuals"],
            "additionalProperties": False
        },
        options={'temperature': float(temperature)},
    )

    json_content = res['message']['content']
    try:
        return json.loads(json_content)
    except JSONDecodeError:
        return {'unparseable': json_content}