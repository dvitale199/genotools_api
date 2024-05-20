FROM python:3.11.3
LABEL maintainer="Dan Vitale <dan@datatecnica.com>"

# Create a non-root user early to avoid running commands as root
RUN adduser --disabled-password --gecos "" gtuser

# Set the working directory
WORKDIR /app

# Update package list and install git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/dvitale199/genotools_api.git

# Change to the app directory
WORKDIR /app/genotools_api

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install .

# Expose port 8080
EXPOSE 8080

# Start the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
