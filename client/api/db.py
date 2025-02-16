from aperturedb import Connector

client = Connector.Connector(
    host="<database instance name or IP without http://>",
    user="admin",
    password="<YOUR_PASSWORD>",
)
client.query([{"GetStatus": {}}])
