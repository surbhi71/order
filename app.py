
from flask import Flask, request, jsonify
from pymongo import MongoClient
import uuid

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient('mongodb://root:password@ecp-cd-mongo-headless.lcm-mongo.svc.cluster.local:27017/?replicaSet=rs0')

db = client['test']
collection = db['order']


@app.route('/updateOrderStatus', methods=['POST'])
def add_product():
    # Get data from request
    data = request.json

    inserted_order = collection.insert_one(data)
    # Return the inserted document ID
    return jsonify({'status': 'success', 'message': 'order status updated'}), 201


@app.route('/order/<id>', methods=['GET'])
def get_product(id):
    # Query MongoDB for the product with the given product_id
    
    for x in collection.find({ "order_id": id}):
        x['_id'] = str(x['_id']) 
        print(x)

    if x:
        del x["_id"]
        return jsonify(x), 200
    else:
        # If the product is not found, return an error message
        return jsonify({'status': 'failure', 'message': 'Order not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
    #app.run(debug=True)

