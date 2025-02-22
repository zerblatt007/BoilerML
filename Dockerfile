# Use a base Python image
FROM python:3.12

# Install dependencies
RUN pip install --no-cache-dir scikit-learn joblib numpy

# Copy your script to the container
COPY noiler_ml/boiler_ml.py /app/boiler_ml.py

# Set the working directory
WORKDIR /app

# Run the Python script when the container starts
CMD ["python", "boiler_ml.py"]

