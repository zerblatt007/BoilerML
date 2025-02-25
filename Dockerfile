# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (including jq)
RUN apt-get update && apt-get install -y jq

# Copy all files and subdirectories from boiler_ml to /app
COPY boiler_ml /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ensure run.sh has execution permissions
RUN chmod +x /app/run.sh

# Run the script when the container starts
CMD [ "/bin/bash", "/app/run.sh" ]

