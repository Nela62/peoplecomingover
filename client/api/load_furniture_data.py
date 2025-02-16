import os
from aperturedb.cli.ingest import from_csv, TransformerType, IngestType

def main():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Load furniture images with CLIP embeddings
    print("Loading furniture images...")
    from_csv(
        filepath="data/furniture_images.adb.csv",
        ingest_type=IngestType.IMAGE,
        transformer=[
            TransformerType.clip_pytorch_embeddings,
            TransformerType.image_properties,
            TransformerType.common_properties
        ]
    )
    
    # Load furniture categories
    print("Loading furniture categories...")
    from_csv(
        filepath="data/furniture_categories.adb.csv",
        ingest_type=IngestType.ENTITY,
    )
    
    # Load connections between furniture and categories
    print("Loading furniture-category connections...")
    from_csv(
        filepath="data/furniture_connections.adb.csv",
        ingest_type=IngestType.CONNECTION,
    )

if __name__ == "__main__":
    main()
