# Use an official Python runtime as a parent image. This image is a slim version of Python 3.9 to keep the image size small.
FROM python:3.9-slim

# Set the working directory in the container to /app.
WORKDIR /app

# Copy the current directory contents (all files and subdirectories) into the container at /app.
COPY . .

# Install any needed packages specified in requirements.txt.
# The --no-cache-dir option prevents pip from caching the packages, which keeps the image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container.
# This means the container will listen on port 5000 for incoming connections.
EXPOSE 5000

# Define the command to run the Flask application.
# This command tells Flask to run the application on all network interfaces (0.0.0.0) and on port 5000.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
