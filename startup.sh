#!/bin/bash

echo "Downloading model zip..."
gdown --id 17PfNRXeIy0xtKBLM3XKh38oyUuiPI1mM -O mental_health_bud.zip

echo "Unzipping model..."
unzip -o mental_health_bud.zip -d .

echo "Starting API..."
uvicorn main:app --host=0.0.0.0 --port=10000
