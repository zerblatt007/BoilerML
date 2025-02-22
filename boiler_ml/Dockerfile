ARG BUILD_FROM=ghcr.io/hassio-addons/base:14.0.4
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install dependencies
RUN apk add --no-cache python3 py3-pip

# Copy add-on files
WORKDIR /app
COPY run.sh .
COPY boiler_ml.py .

# Install Python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set permissions
RUN chmod +x /app/run.sh

CMD [ "/app/run.sh" ]

