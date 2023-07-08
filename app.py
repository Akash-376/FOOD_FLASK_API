from flask import Flask, request, jsonify
# from flask_cors import CORS # to handle CORS policy error

app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
my_data = []

my_orders = []


'''
http://127.0.0.1:5000/dishes
body
{
    "dish_id": 333,
    "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ39g0nTEgdgIFYFYPkvzDRav-lJd4rMBVDVc19Gd9iVw&s",
    "dish_name": "Burger",
    "price": 100,
    "availability": false
}
'''

# add new Dish
@app.route('/dishes', methods=['POST'])
def add_item():

    new_item = {
        'dish_id': request.json['dish_id'],
        'image': request.json['image'],
        'dish_name': request.json['dish_name'],
        'price': request.json['price'],
        'availability': request.json['availability']
    
    }

    my_data.append(new_item)
    return jsonify(new_item)

# get all dishes
@app.route('/dishes')
def get_all_dishes():
    if len(my_data) == 0:
        jsonify({'success': False,'message' : 'Not any Dish available yet!'})
    return jsonify(my_data)
    

# get specific dish by dish_id
@app.route('/dishes/<int:dish_id>')
def get_dish(dish_id):
    for dish in my_data:
        if dish['dish_id'] == dish_id:
            return jsonify(dish)
    return {'success': False,'message': 'dish not found with this Id'}



# update specific dish by dish_id
@app.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    for dish in my_data:
        if dish['dish_id'] == dish_id:

            dish['dish_id'] =  dish_id
            dish['image'] =  request.json['image']
            dish['dish_name'] =  request.json['dish_name']
            dish['price'] =  request.json['price']
            dish['availability'] =  request.json['availability']
            return jsonify(dish)
    return {'success': False,'error': 'dish not found'}



# http://127.0.0.1:5000/dishes/1?availability=False/True
# update availability status of a specific dish by dish_id
@app.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish_availability(dish_id):
    for dish in my_data:
        if dish['dish_id'] == dish_id:

            dish['availability'] =  request.args.get('availability')
            return jsonify(dish)
    return {'success': False,'error': 'dish not found'}

# Delete dish by Id
@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    for dish in my_data:
        if dish['dish_id'] == dish_id:
            my_data.remove(dish)
            return jsonify({'success': True, 'message': 'Dish removed from the menu successfully!'})
    return jsonify({'success': False, 'message': 'Dish not found in the menu!'})

orderIdGenerator = 1

# function to take order from customers
@app.route('/orders/<int:dish_id>', methods = ['POST'])
def place_order(dish_id):
    global orderIdGenerator
    for dish in my_data:
        if dish['dish_id'] == dish_id:
            if dish['availability'] == True:
                order = {**dish}
                order['order_id'] = orderIdGenerator
                order['customer name'] = request.json['customer name']
                order['order_status'] = 'Pending'
                orderIdGenerator += 1
                my_orders.append(order)
            else:
                return jsonify({'success': False,'message' : 'Sorry! this Dish is Currently Unavailable'})
            return jsonify({'success': True,'message' : 'Order placed Successfully'})
    return jsonify({'success': False,'message' : 'Invalid Dish Id'})


# get all orders
@app.route('/orders')
def get_all_orders():
    if len(my_orders) == 0:
        return jsonify({'success': False,'message' : 'Not any order found'})
    return jsonify(my_orders)


# get specific order by order_id
@app.route('/orders/<int:order_id>')
def get_order(order_id):
    for order in my_orders:
        if order['order_id'] == order_id:
            return jsonify(order)
    return {'success': False,'message': 'dish not found with this Id'}

# http://127.0.0.1:5000/orders/1?order_status=delivered
# update availability status of a specific dish by dish_id
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    for order in my_orders:
        if order['order_id'] == order_id:

            order['order_status'] =  request.args.get('order_status')
            return jsonify(order)
    return {'success': False,'error': 'order not found'}



if __name__ == '__main__':
    app.run(host = "0.0.0.0")