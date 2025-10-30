# image-description - Playing around with multimodal LLMs for image description

This repository contains some code to use the [Gemma3](https://ollama.com/library/gemma3)
open-source multimodal LLM to describe images stored in a directory. Additional metadata
can be provided in two ways:
* For an image named `image.jpg`, a `image.txt` file in the same directory.
* A `metadata.txt` file in any of the parent directories of the image, going back to the file root.

Descriptions are returned as JSON, and are written to `image.json` in the same directory as
the image file. See [images/Galapagos-interactions](./images/Galapagos-interactions) for some
examples.

This script uses [Ollama](https://ollama.com/) to call the LLM, and works on macOS.