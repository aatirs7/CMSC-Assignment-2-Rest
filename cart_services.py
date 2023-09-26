from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# In-memory database for carts
# Structure: {user_id: {product_id: quantity}}
carts = {}

PRODUCT_SERVICE_URL = 'http://127.0.0.1:5000/products'

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = carts.get(user_id, {})
    response = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = requests.get(f'{PRODUCT_SERVICE_URL}/{product_id}').json()
        total_price += product['price'] * quantity
        response.append({
            'name': product['name'],
            'quantity': quantity,
            'total_price': product['price'] * quantity
        })
    return jsonify({'cart': response, 'total_price': total_price})

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)
    cart = carts.setdefault(user_id, {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    return jsonify({'message': 'Product added to cart', 'cart': cart})

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    cart = carts.get(user_id, {})
    if product_id in cart:
        quantity_to_remove = request.json.get('quantity', cart[product_id])
        cart[product_id] -= quantity_to_remove
        if cart[product_id] <= 0:
            del cart[product_id]
    return jsonify({'message': 'Product removed from cart', 'cart': cart})

if __name__ == '__main__':
    app.run(debug=True, port=5001)