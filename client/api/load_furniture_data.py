import os
import subprocess

def install_requirements():
    """Install required packages"""
    subprocess.check_call(["pip", "install", "git+https://github.com/openai/CLIP.git"])
    subprocess.check_call(["pip", "install", "facenet-pytorch", "--no-deps"])

def main():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Change to data directory
    os.chdir('data')
    
    try:
        # Generate the CSV files
        subprocess.check_call(["python", "../scripts/convert_furniture_data.py"])
        
        # Install requirements
        install_requirements()
        
        # Import after installing requirements
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
    
    finally:
        # Change back to original directory
        os.chdir('..')

if __name__ == "__main__":
    main()
