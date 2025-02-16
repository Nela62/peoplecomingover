#!/bin/bash

# Create data directory
mkdir -p data
cd data

# Generate the CSV files
python ../scripts/convert_furniture_data.py

# Install required packages
pip install git+https://github.com/openai/CLIP.git
pip install facenet-pytorch --no-deps

# Run the ingestion
python -c "
from aperturedb.cli.ingest import from_csv, TransformerType, IngestType

# Load furniture images with CLIP embeddings
print('Loading furniture images...')
from_csv(
    filepath='furniture_images.adb.csv',
    ingest_type=IngestType.IMAGE,
    transformer=[
        TransformerType.clip_pytorch_embeddings,
        TransformerType.image_properties,
        TransformerType.common_properties
    ]
)

# Load furniture categories
print('Loading furniture categories...')
from_csv(
    filepath='furniture_categories.adb.csv',
    ingest_type=IngestType.ENTITY,
)

# Load connections between furniture and categories
print('Loading furniture-category connections...')
from_csv(
    filepath='furniture_connections.adb.csv',
    ingest_type=IngestType.CONNECTION,
)
"

cd -
