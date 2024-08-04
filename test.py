import json

from flask import Flask, request, jsonify

app = Flask(__name__)

AUTH_URI = '/auth_bot'
GET_ACTIONS_URI = '/get_bot_actions'
REMOVE_ACTION_URI = '/remove_action'


@app.route(GET_ACTIONS_URI, methods=['GET'])
def test_tak_request():
    with open("test_auth.json") as f_in:
        data = json.load(f_in)

    return jsonify(data), 200


@app.route(REMOVE_ACTION_URI, methods=['DELETE'])
def remove_task():
    gotten_data = request.json
    with open("test_auth.json") as f_in:
        response = json.load(f_in)
    if not 'actions' in response.keys(): return False  # проверяем пришедший список действий не пуст?
    actions = response['actions']

    gotten_data(gotten_data)
    actions.pop()


@app.route("/confirm", methods=['POST'])
def confirm():
    print(request.json)
    return "OK"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=57424)
