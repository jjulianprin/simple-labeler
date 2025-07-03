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

# Copying src folder into the container
COPY ./src /app/src

#Bringing the images from a S3 bucket
RUN mkdir -p /app/FOLDER_A && \
    mkdir -p /app/FOLDER_B && \
    aws s3 sync s3://<s3-Bucket>/<ObjectPath> /app/FOLDER_A && \
    aws s3 sync s3://<s3-Bucket>/<ObjectPath> /app/FOLDER_B

# Creating venv and installing dependencies
RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r ./src/requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Command to run your Streamlit app
ENTRYPOINT ["streamlit", "run"]
CMD ["./src/image_labeling_app.py"]