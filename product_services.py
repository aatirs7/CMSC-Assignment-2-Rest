from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database
products = {}
counter = 1

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(list(products.values()))

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify(product)

@app.route('/products', methods=['POST'])
def add_product():
    global counter
    data = request.get_json()
    product = {
        'id': counter,
        'name': data['name'],
        'price': data['price'],
        'quantity': data['quantity']
    }
    products[counter] = product
    counter += 1
    return jsonify(product), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)