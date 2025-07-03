# opc-ogsub-geo-ml-interpretation

This project provides a simple image labeling tool using Streamlit, designed for machine learning interpretation tasks in geoscience.

## Getting Started

### Running Locally

To start the Streamlit app locally, run:

```bash
streamlit run src/image_labeling_app.py
```

### Using Docker

#### Build the Docker image

```bash
docker buildx build -t simple-labeler .
```

#### Run the container (detached mode)

```bash
docker run -d --name simple-labeler -v ./image_stats.json:/app/image_stats.json -p 8501:8501 simple-labeler
```

#### Run the container (interactive debug mode)

```bash
docker run -it --rm --name simple-labeler -v ./image_stats.json:/app/image_stats.json -p 8501:8501 --entrypoint bash simple-labeler
```

## Image Statistics

The `image_stats.json` file is used to store statistics about image labeling guesses. This file will be empty in the repository but will be populated by the app as users interact with it.

Example structure:

```json
{
    "FOLDER_A/5000c.JPG": { "correct": 1, "incorrect": 0 },
    "FOLDER_A/5000a.JPG": { "correct": 2, "incorrect": 1 },
    "FOLDER_B/300a.JPG": { "correct": 0, "incorrect": 1 },
    "FOLDER_B/300d.JPG": { "correct": 1, "incorrect": 0 },
    "FOLDER_B/300b.JPG": { "correct": 2, "incorrect": 2 },
    "FOLDER_A/5000b.JPG": { "correct": 0, "incorrect": 1 },
    "FOLDER_A/5000d.JPG": { "correct": 0, "incorrect": 1 },
    "FOLDER_B/300c.JPG": { "correct": 1, "incorrect": 1 }
}
```

Each entry tracks the number of correct and incorrect guesses for each image.

---