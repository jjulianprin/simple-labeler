FROM amazonlinux:2023 as base

# Install necessary system packages
RUN dnf update -y && \
    dnf install -y python3-pip \
                   awscli \
                   tar \
                   unzip \
                   jq \
                   git && \
    dnf clean all

# Set working directory in the container
WORKDIR /app

# Copying files into the container
COPY requirements.txt .
COPY image_labeling_app.py .

#Bringing the images from a S3 bucket
RUN mkdir -p /app/holstein && \
    mkdir -p /app/syn2seis && \
    aws s3 sync s3://<bucketName>/folderA /app/folderA && \
    aws s3 sync s3://<bucketName>/folderB /app/folderB

# Creating venv and installing dependencies
RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Command to run your Streamlit app
ENTRYPOINT ["streamlit", "run"]
CMD ["image_labeling_app.py"]