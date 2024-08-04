import json
import logging

from flask import Flask, Response, request, jsonify
from os import getenv

app = Flask(__name__)
logger = logging.getLogger(__name__)

AUTH_URI = '/auth_bot'
GET_ACTIONS_URI = '/get_bot_actions'
REMOVE_ACTION_URI = '/remove_action'

legal_bots_list = ['telegram']

@app.route(GET_ACTIONS_URI+'/<bot_id>', methods=['GET'])
def test_tak_request(bot_id):
    with open("test_auth.json") as f_in:
        data = json.load(f_in)

    return jsonify(data), 200


@app.route(REMOVE_ACTION_URI+'/<bot_id>', methods=['DELETE'])
def remove_task(bot_id):
    if bot_id not in legal_bots_list:
        return Response("Permission denied: bot_id is not in list", status=403)


    gotten_data = request.json
    with open("test_auth.json") as f_in:
        response = json.load(f_in)
    if not 'actions' in response.keys(): return False  # проверяем пришедший список действий не пуст?
    actions = response['actions']

    gotten_data(gotten_data)
    actions.pop()


@app.route("/confirm", methods=['POST'])
def confirm():
    with open("test_auth.json", 'r') as f_in:
        tasks = json.load(f_in)["data"]

    data = request.json
    new_tasks = tasks.copy()

    for task_ind in range(len(tasks)):
        if tasks[task_ind]["message_id"] == data["message_id"]:
            new_tasks.pop(task_ind)
    
    with open("test_auth.json", 'w') as f_out:
        json.dump({"data": new_tasks}, f_out)
    return "OK"


if __name__ == "__main__":
    app.run(host=getenv("SERVER_URI"), port=int(getenv("SERVER_PORT")))
