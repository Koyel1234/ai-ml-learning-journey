#use python 3.11 base image
FROM python:3.11-slim

# set working directory
WORKDIR /app

# Copy requirements  and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port the app runs on
EXPOSE 8000

# Command to start FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


