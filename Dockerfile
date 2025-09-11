# Use the official Python base image from the Docker Hub
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies from requirements.txt
# Using --no-cache-dir to save space
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Command to run your Python script
# This command is a placeholder, as the actual command will be set in the docker-compose.yml
CMD ["tail", "-f", "/dev/null"]