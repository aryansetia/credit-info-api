FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

# Set environment variables
ENV DATABASE_URL=postgresql://postgres:postgres@localhost/credit-info

# Expose port 8000 for the FastAPI app
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
