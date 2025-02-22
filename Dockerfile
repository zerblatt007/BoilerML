# Use a base Python image
FROM python:3.12

# Install dependencies
RUN pip install --no-cache-dir scikit-learn joblib numpy

# Copy your script to the container
COPY boiler_ml/boiler_ml.py /app/boiler_ml.py

# Copy the model file to the container
COPY boiler_ml/models/boiler_ml_model_f2.pkl /app/models/boiler_ml_model_f2.pkl

# Set the working directory
WORKDIR /app

# Run the Python script when the container starts
CMD ["python", "boiler_ml.py"]

