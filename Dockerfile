# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory into the container
COPY src/ src/

# Set environment variables
ENV DATABASE_URL=postgresql://postgres:postgres@localhost/credit-info

# # This will run when you build the Docker image
# RUN python src/insert_dump.py

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
