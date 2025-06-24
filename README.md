# simple-labeler

**simple-labeler** is an interactive image labeling application built with Streamlit. It allows users to label images sourced from local folders or remote object storage (such as AWS S3).

## Features

- Loads image file paths from specified local folders or S3 buckets.
- Supports common image formats: `.png`, `.jpg`, `.jpeg`.
- Presents an intuitive labeling interface via Streamlit.
- Dockerized for easy deployment.

## How It Works

1. The app scans the folders defined by `FOLDER_A` and `FOLDER_B` (local or S3).
2. It collects all image files and pairs each image path with its source folder.
3. Users can label images through the web interface.

## Getting Started

### Prerequisites

- Docker installed on your machine
- AWS credentials configured (if using S3)
- Access to the required S3 buckets or local folders

### Build the Docker Image

Replace `<bucketName>` in the Dockerfile with your actual S3 bucket name if using S3.

```bash
docker buildx build -t image_labeling_app .
```

### Run the Application

```bash
docker run -d --name python-temp -p 8501:8501 image_labeling_app
```

The app will be available at [http://localhost:8501](http://localhost:8501).

---

For more details, refer to the source code and comments within the repository.
