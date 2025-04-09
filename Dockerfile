# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
# Use --trusted-host to avoid potential SSL issues in some environments
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 8000 available to the world outside this container (if we add an API later)
# EXPOSE 8000

# Define environment variable (optional, can be overridden)
# ENV NAME World

# Run main.py when the container launches
# Use python -u for unbuffered output, helpful for seeing logs in real-time
ENTRYPOINT ["python", "-u", "main.py"] 