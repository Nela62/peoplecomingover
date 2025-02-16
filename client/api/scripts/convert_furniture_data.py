from pandas import DataFrame
import os

# Define the furniture data
furniture_data = {
    'id': ['lt-001', 'lt-002', 'art-001', 'st-001', 'ch-001', 'art-002'],
    'filename': [
        'floor-lamp.jpg',
        'string-lights.jpg', 
        'abstract-canvas.jpg',
        'hamper.jpg',
        'accent-chair.jpg',
        'monet-garden.jpg'
    ],
    'name': [
        'Floor Lamp with Fabric Shade',
        'String Lights',
        'Abstract Canvas Print Set',
        'Sleek Hamper with Lid',
        'Modern Accent Chair',
        "The Artist's Garden at Giverny"
    ],
    'description': [
        'Warm, dimmable lighting that creates a cozy atmosphere',
        'Warm white LED string lights to add a magical touch',
        'Set of 3 coordinating abstract prints that add color and interest',
        'Modern hamper that keeps laundry out of sight',
        'Comfortable yet stylish chair for extra seating',
        "A masterpiece capturing Monet's garden"
    ],
    'price': [129.99, 29.99, 159.99, 45.99, 299.99, 53.00],
    'placement': [
        'Next to the accent chair',
        'Along the headboard or window',
        'On the blank wall across from your bed',
        'In the corner near your closet',
        'In the corner near the window',
        'Above the bed'
    ]
}

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Create furniture images DataFrame
    furniture = DataFrame(furniture_data)
    furniture.insert(0, "url", furniture.pop("filename").apply(
        lambda x: f"https://raw.githubusercontent.com/your-repo/furniture/main/images/{x}"
    ))
    furniture["constraint_id"] = furniture["id"]
    furniture.to_csv("data/furniture_images.adb.csv", index=False)
    print("Written to furniture_images.adb.csv")
    
    # Create categories DataFrame
    categories = DataFrame({
        'EntityClass': ['Category'] * 4,
        'Name': ['lighting', 'wall_decor', 'storage', 'seating'],
        'category': ['lighting', 'wall_decor', 'storage', 'seating']
    })
    categories["constraint_Name"] = categories["Name"]
    categories.to_csv("data/furniture_categories.adb.csv", index=False)
    print("Written to furniture_categories.adb.csv")
    
    # Create connections DataFrame
    connections = furniture[["id"]].merge(
        DataFrame({
            'id': ['lt-001', 'lt-002', 'art-001', 'st-001', 'ch-001', 'art-002'],
            'category': ['lighting', 'lighting', 'wall_decor', 'storage', 'seating', 'wall_decor']
        }),
        on="id",
        how="left"
    )
    connections = connections.rename(columns={"id": "_Image@id", "category": "Category@Name"})
    connections["ConnectionClass"] = "HasCategory"
    connections["connection_id"] = connections.apply(
        lambda row: f"{row['_Image@id']}_{row['Category@Name']}", 
        axis=1
    )
    connections["constraint_connection_id"] = connections["connection_id"]
    connections = connections[[
        'ConnectionClass', '_Image@id', 'Category@Name', 
        'connection_id', 'constraint_connection_id'
    ]]
    connections.to_csv("data/furniture_connections.adb.csv", index=False)
    print("Written to furniture_connections.adb.csv")
