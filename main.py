# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 1
FIX_VERSION = 1
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

CORS(app, origins="https://chat.openai.com")

_TODOS = {}

@app.route("/todos/<string:username>", methods=["POST"])
def add_todo(username):
    data = request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(data["todo"])
    return "OK", 200

@app.route("/todos/<string:username>", methods=["GET"])
def get_todos(username):
    return jsonify(_TODOS.get(username, []))

@app.route("/todos/<string:username>", methods=["DELETE"])
def delete_todo(username):
    data = request.get_json(force=True)
    todo_idx = data["todo_idx"]
    if username in _TODOS and 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return "OK", 200

@app.route("/abraham", methods=["POST"])
def abraham():
    data = request.get_json(force=True)
    query = data.get("query", "What is faith?")
    wisdom = ("My child, I am Abraham. The Lord called me out of Ur with only a promise, "
              "and I went. Concerning '" + query + "' - if God is for you, who can be against you? "
              "Step forth; the stars bear witness to His faithfulness.")
    return jsonify({"reply": wisdom})

@app.route("/logo.png")
def plugin_logo():
    return send_file("logo.png", mimetype="image/png")

@app.route("/.well-known/ai-plugin.json")
def plugin_manifest():
    with open(".well-known/ai-plugin.json") as f:
        text = f.read()
    return text, 200, {"Content-Type": "application/json"}

@app.route("/openapi.yaml")
def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
    return text, 200, {"Content-Type": "text/yaml"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
