# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install system dependencies for Pillow and other packages
RUN apt-get update && apt-get install -y \
    zlib1g-dev libjpeg-dev libpng-dev \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Streamlit app files into the container
COPY . /app

# Expose the port that Streamlit runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
