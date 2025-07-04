# Base Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose the port your app runs on (e.g., 8000 for FastAPI)
EXPOSE 8000

# Command to run the app (change to fit your app)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
