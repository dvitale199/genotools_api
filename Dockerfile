# Base image with essential dependencies
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements and project files
# COPY requirements.txt /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install the_real_genotools && \
    pip install uvicorn && \
    pip install fastapi && \
    pip install google-cloud-batch

# Expose port for Streamlit
# EXPOSE 8080
# Expose port for FastAPI
EXPOSE 8000

# run fastapi app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Start Streamlit app
# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]