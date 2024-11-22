# GenoTools API

This project provides a RESTful API interface to the [GenoTools](https://github.com/dvitale199/GenoTools) package, allowing users to perform genomic data quality control and analysis through HTTP requests. The API handles data transfer from Google Cloud Storage (GCS), executes GenoTools commands, and returns the results, facilitating integration with other services and automation of genomic workflows.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Example Request](#example-request)
  - [Parameters](#parameters)
  - [Response](#response)
- [Testing](#testing)
- [Docker Usage](#docker-usage)
  - [Building the Docker Image](#building-the-docker-image)
  - [Running the Docker Container](#running-the-docker-container)
  - [Accessing the API](#accessing-the-api)
- [Environment Variables](#environment-variables)
- [License](#license)

## features

- **run genotools commands**: Execute GenoTools commands remotely via API calls.
- **data handling with gcs**: Download input files from GCS and upload results back to GCS.
- **API Key Authentication**: Secure endpoints using API key authentication.
- **Flexible Parameters**: Support for various GenoTools parameters and options.
- **Dockerized Deployment**: Easy deployment using Docker.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (if interacting with GCS)
- GenoTools package (`the-real-genotools`)
- Docker (optional, for containerized deployment)
- Poetry (for dependency management)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/genotools-api.git
   cd genotools-api
   ```

2. **Install Dependencies**
Ensure you have Poetry installed.

```
poetry install
```

3. **set up environment**
create .env file in the project root direcotry and define the variables
```
API_KEY_NAME=your_api_key_name
API_KEY=your_api_key_value
```

## Configuration

- **API Key Authentication**

  - The API uses API key authentication via a custom header.
  - Set `API_KEY_NAME` to the header name you want to use (e.g., `X-API-KEY`).
  - Set `API_KEY` to the secret key clients must provide.

- **Google Cloud Credentials**

  - Ensure the application has access to Google Cloud credentials if interacting with GCS.
  - Set up authentication by configuring the `GOOGLE_APPLICATION_CREDENTIALS` environment variable or using default application credentials.

## Usage

### API Endpoints

#### `GET /`

- **Description**: Health check endpoint.
- **Response**: `"Welcome to GenoTools"`

#### `POST /run-genotools/`

- **Description**: Execute a GenoTools command with specified parameters.
- **Authentication**: Requires API key in the header.
- **Request Body**: JSON object with parameters as defined in the `GenoToolsParams` model.
- **Response**: JSON object containing the execution result.

### Example Request

Here's how to use the API to run a GenoTools command:

**Python Script (`test_main.py`):**

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = 'http://0.0.0.0:8080/run-genotools/'

payload = {
    "pfile": "gs://your_bucket/your_pfile_prefix",
    "out": "gs://your_bucket/output_prefix",
    "callrate": 0.5,
    "sex": True,
    "storage_type": "gcs"
}

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")

headers = {
    API_KEY_NAME: API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.json())
```

**Environment Variables (`.env`):**

```env
API_KEY_NAME=X-API-KEY
API_KEY=your_api_key_value
```

### Parameters

The `GenoToolsParams` model supports the following fields:

- **Input Files:**
  - `bfile`: Path to PLINK binary fileset.
  - `pfile`: Path to PLINK 2 binary fileset.
  - `vcf`: Path to VCF file.
- **Output:**
  - `out`: Output file prefix.
- **Options:**
  - `full_output`: `bool` (optional)
  - `skip_fails`: `bool` (optional)
  - `warn`: `bool` (optional)
  - `callrate`: `float` or `bool` (optional); call rate threshold.
  - `sex`: `bool` (optional); perform sex checks.
  - `related`: `bool` (optional); check for relatedness.
  - `related_cutoff`: `float` (optional)
  - `duplicated_cutoff`: `float` (optional)
  - `prune_related`: `bool` (optional)
  - `prune_duplicated`: `bool` (optional)
  - `het`: `bool` (optional)
  - `all_sample`: `bool` (optional)
  - `all_variant`: `bool` (optional)
  - `maf`: `float` (optional)
  - `ancestry`: `bool` (optional); perform ancestry inference.
  - `ref_panel`: `str` (optional); path to reference panel.
  - `ref_labels`: `str` (optional); path to reference labels.
  - `model`: `str` (optional); path to ML model for ancestry prediction.
  - `storage_type`: `'local'` or `'gcs'`; storage location of files.

### Response

A successful response will include:

- `"message"`: Status message (e.g., `"Job submitted"`).
- `"command"`: The GenoTools command executed.
- `"result"`: Output from the command execution.

## Testing

To run the provided test script:

1. **Ensure the API is Running**

   ```bash
   uvicorn genotools_api.main:app --host 0.0.0.0 --port 8080

2. **Run the Test Script**

   ```bash
   python test_main.py
   ```

3. **check the output**
The script will print the HTTP status code and response JSON.

## docker usage

** build image and run docker container **
```
docker build -t genotools-api .

docker run -d -p 8080:8080 \
  -e API_KEY_NAME="X-API-KEY" \
  -e API_KEY="your_api_key_value" \
  --name genotools-api \
  genotools-api
```


Maintainer: Dan Vitale (dan@datatecnica.com)
