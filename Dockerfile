# Base image with essential dependencies
FROM python:3.11

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8080

# Command to run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]