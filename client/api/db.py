from aperturedb import Connector

client = Connector.Connector(
    host="<database instance name or IP without http://>",
    user="admin",
    password="<YOUR_PASSWORD>",
)

def add_connection(src_ref, dst_ref, connection_class, properties=None):
    """Add a connection between two objects in ApertureDB.
    
    Args:
        src_ref: Source reference ID
        dst_ref: Destination reference ID 
        connection_class: Class name for the connection (e.g. "contains", "related_to")
        properties: Optional dict of connection properties
    """
    query = [{
        "AddConnection": {
            "class": connection_class,
            "src": src_ref,
            "dst": dst_ref,
            "properties": properties or {}
        }
    }]
    return client.query(query)

def find_connections(connection_class=None, properties=None):
    """Find connections in the database.
    
    Args:
        connection_class: Optional class name to filter by
        properties: Optional dict of property constraints
    """
    query = [{
        "FindConnection": {
            **({"with_class": connection_class} if connection_class else {}),
            **({"constraints": properties} if properties else {}),
            "results": {
                "all_properties": True
            }
        }
    }]
    return client.query(query)

def delete_connection(connection_class=None, properties=None):
    """Delete connections matching the criteria.
    
    Args:
        connection_class: Optional class name to filter by
        properties: Optional dict of property constraints to match
    """
    query = [{
        "DeleteConnection": {
            **({"with_class": connection_class} if connection_class else {}),
            **({"constraints": properties} if properties else {})
        }
    }]
    return client.query(query)

# Initialize connection
client.query([{"GetStatus": {}}])
