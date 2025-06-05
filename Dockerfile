# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose any ports if needed (optional)
# EXPOSE 8000

# Set environment variables if needed
ENV PYTHONUNBUFFERED=1

# Run the main application
CMD ["python", "-m", "iv_spike_notifier.app.main"]
