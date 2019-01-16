import os
import uuid

# import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

TODOS = [
    {
        'id': uuid.uuid4().hex,
        'todo': 'On the Road',
        'assignee': 'Jack Kerouac',
        'done': True
    },
    {
        'id': uuid.uuid4().hex,
        'todo': 'Harry Potter and the Philosopher\'s Stone',
        'assignee': 'J. K. Rowling',
        'done': False
    },
    {
        'id': uuid.uuid4().hex,
        'todo': 'Green Eggs and Ham',
        'assignee': 'Dr. Seuss',
        'done': True
    }
]


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/TODOS', methods=['GET', 'POST'])
def all_TODOS():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        TODOS.append({
            'id': uuid.uuid4().hex,
            'todo': post_data.get('todo'),
            'assignee': post_data.get('assignee'),
            'done': post_data.get('done')
        })
        response_object['message'] = 'todo added!'
    else:
        response_object['TODOS'] = TODOS
    return jsonify(response_object)


@app.route('/TODOS/<todo_id>', methods=['GET', 'PUT', 'DELETE'])
def single_todo(todo_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        # TODO: refactor to a lambda and filter
        return_todo = ''
        for todo in TODOS:
            if todo['id'] == todo_id:
                return_todo = todo
        response_object['todo'] = return_todo
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_todo(todo_id)
        TODOS.append({
            'id': uuid.uuid4().hex,
            'todo': post_data.get('todo'),
            'assignee': post_data.get('assignee'),
            'done': post_data.get('done')
        })
        response_object['message'] = 'todo updated!'
    if request.method == 'DELETE':
        remove_todo(todo_id)
        response_object['message'] = 'todo removed!'
    return jsonify(response_object)


# @app.route('/charge', methods=['POST'])
# def create_charge():
#     post_data = request.get_json()
#     amount = round(float(post_data.get('todo')['price']) * 100)
#     stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
#     charge = stripe.Charge.create(
#         amount=amount,
#         currency='usd',
#         card=post_data.get('token'),
#         description=post_data.get('todo')['todo']
#     )
#     response_object = {
#         'status': 'success',
#         'charge': charge
#     }
#     return jsonify(response_object), 200
#
#
# @app.route('/charge/<charge_id>')
# def get_charge(charge_id):
#     stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
#     response_object = {
#         'status': 'success',
#         'charge': stripe.Charge.retrieve(charge_id)
#     }
#     return jsonify(response_object), 200


def remove_todo(todo_id):
    for todo in TODOS:
        if todo['id'] == todo_id:
            TODOS.remove(todo)
            return True
    return False


if __name__ == '__main__':
    app.run()
