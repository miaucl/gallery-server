# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir waitress

# Copy the rest of the application code into the container
COPY . .

# Expose the port the Flask app runs on
EXPOSE 8080

# Define the command to run the application
CMD ["python", "-m", "gallery_server"]
