# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port (FastAPI runs on 80 inside container)
EXPOSE 80

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
