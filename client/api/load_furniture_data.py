from pandas import DataFrame
from aperturedb.cli.ingest import from_csv, TransformerType, IngestType
import os

# Define the furniture data
furniture_data = {
    'EntityClass': ['Furniture'] * 6,
    'Name': [
        'Floor Lamp with Fabric Shade',
        'String Lights',
        'Abstract Canvas Print Set',
        'Sleek Hamper with Lid',
        'Modern Accent Chair',
        "The Artist's Garden at Giverny"
    ],
    'category': [
        'lighting',
        'lighting',
        'wall_decor',
        'storage',
        'seating',
        'wall_decor'
    ],
    'price': [
        129.99,
        29.99,
        159.99,
        45.99,
        299.99,
        53.00
    ],
    'description': [
        'Warm, dimmable lighting that creates a cozy atmosphere',
        'Warm white LED string lights to add a magical touch',
        'Set of 3 coordinating abstract prints that add color and interest',
        'Modern hamper that keeps laundry out of sight',
        'Comfortable yet stylish chair that provides extra seating without taking up too much space',
        "A masterpiece capturing the serene beauty of Monet's garden with vibrant colors and impressionistic style"
    ],
    'image_url': [
        'https://m.media-amazon.com/images/I/61pJwYkeP9L._AC_SL1001_.jpg',
        'https://m.media-amazon.com/images/I/81wGn2TQJeL._AC_SL1500_.jpg',
        'https://m.media-amazon.com/images/I/91qqiXudI0L._AC_SL1500_.jpg',
        'https://m.media-amazon.com/images/I/71-jCUaVwKL._AC_SL1500_.jpg',
        'https://m.media-amazon.com/images/I/81KuAZKVGKL._AC_SL1500_.jpg',
        'https://www.claude-monet.com/assets/img/paintings/the-artists-garden-at-giverny.jpg'
    ],
    'placement': [
        'Next to the accent chair - perfect for reading or creating ambient lighting',
        'Along the headboard or window - creates a warm, inviting atmosphere',
        'On the blank wall across from your bed - creates a focal point and add personality',
        'In the corner near your closet',
        'In the corner near the window - creates a nice reading nook and gives guests a place to sit',
        'Above the bed - creates a focal point and adds a touch of elegance'
    ],
    'dimensions': [
        None,
        None,
        '40x60 cm',
        None,
        '70x85x75 cm',
        '36x24 inches'
    ],
    'color_options': [
        'Black/White Shade,Brass/Beige Shade',
        None,
        None,
        'White,Gray,Black',
        'Gray Velvet,Navy Blue,Forest Green',
        None
    ]
}

def main():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Convert to DataFrame
    df = DataFrame(furniture_data)
    
    # Add constraint columns
    df['constraint_Name'] = df['Name']
    
    # Save to CSV
    csv_path = 'data/furniture.adb.csv'
    df.to_csv(csv_path, index=False)
    print(f"Written to {csv_path}")
    
    # Ingest into ApertureDB
    from_csv(
        filepath=csv_path,
        ingest_type=IngestType.ENTITY,
    )

if __name__ == "__main__":
    main()
