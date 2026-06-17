# HARMONIC-Optimizer-Python

[![DOI](https://zenodo.org/badge/1267159607.svg)](https://doi.org/10.5281/zenodo.20729053)

## Introduction
This project contains the API for the HARMONIC-Optimizer-Python. <br>
It is used to receive the data from the Orchestrator and start the optimization process.


## For local development
### Set up virtual environment and install requirements
```bash
pip install -r requirements.txt
```

### Activate the virtual environment
```bash
source .venv/bin/activate
```

### Run the live server
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```


## Docker
### Build the image
```bash
docker build -t <IMAGE-NAME> .
```

### Run the container
```bash
docker run -d --name <CONTAINER-NAME> -p 8001:8001 <IMAGE-NAME>
```

Uvicorn server for the optimizer will be running on **http://localhost:8001**.
