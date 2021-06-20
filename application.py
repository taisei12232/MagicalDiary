from azure.cosmos import exceptions, CosmosClient, PartitionKey
from flask import Flask, jsonify, request
from . import app


# Initialize the Cosmos client
endpoint = "https://agentserver.documents.azure.com:443/"
key = 'xRyACyJ8SEBhfGm7ZdcPThYvpkyPFcMmD8o8iKTDhI8HJUKfByFr0hvoactFQF7bb0Nq1TF12dzxqfWmCjeDBA=='

# <create_cosmos_client>
client = CosmosClient(endpoint, key)
# </create_cosmos_client>

# Create a database
# <create_database_if_not_exists>
database = client.get_database_client('MagicalDiary')
# </create_database_if_not_exists>
print(database)
# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
container_name = 'User'
container = database.get_container_client(container_name)
print(container)

# </create_container_if_not_exists>
@app.route('/')
def all():
    items = container.read_all_items(max_item_count=5)
    print(' --- read_all_items --- ')
    print()
    return jsonify(list(items))
@app.route('/read/<user_id>', methods=['GET'])
def read_user(user_id):
    item = container.read_item(user_id,user_id)
    print(' --- read_item --- ')
    print(item['name'])
    print()
    return item

@app.route('/search/<user_id>', methods=['GET'])
def seach_user(user_id):
    query = f"SELECT * FROM items i WHERE i.id = '{user_id}'"
    items = container.query_items(query, enable_cross_partition_query=True)
    print(' --- query_items 3 --- ')
    print()
    return jsonify(list(items)[0]['name'])

@app.route('/rank')
def ranking():
    query = "SELECT * FROM items i ORDER BY i.count"
    items = container.query_items(query, enable_cross_partition_query=True)
    print(' --- query_items 3 --- ')
    print()
    top = []
    for i in jsonify(list(items)):
        top.append({i['name'],i['id']})
