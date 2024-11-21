# Specify the base image
FROM python:3.12-bullseye

# Set environment variables
# Prevents Python from writing .pyc files and enables unbuffered output for real-time logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# Updates apt and installs necessary libraries for building Python and system dependencies.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libsqlite3-dev \
    zlib1g-dev \
    default-libmysqlclient-dev \
    pkg-config \
    --no-install-recommends && \
    # Remove unnecessary files
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*   

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy files into the working directory
COPY . /app/

# Tell pipenv to create a virtual environment
ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_SYSTEM=1

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Expose the port the app runs on
EXPOSE 8000

# Run the application 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Build the Docker image
# sudo docker build -t leet:test .

# Run the Docker container
# sudo docker run -p 8000:8000 --env-file example.env leet:test

# Run the Docker container in detached mode
# sudo docker run -d -p 8000:8000 --env-file example.env leet:test

# Stop the Docker container
# sudo docker stop <container_id>