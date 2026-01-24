# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 1
FIX_VERSION = 8
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

CORS(app, origins="https://chat.openai.com")
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="https://chat.openai.com")

_TODOS = {}

# Embedded knowledge base for "self-learning" about Abraham
ABRAHAM_KNOWLEDGE = """
Abraham's Path: Born ~2000 BCE in Ur (Iraq), migrated to Haran (Turkey), called to Canaan at 75: Shechem, Bethel, Negev, Egypt (famine), back to Hebron/Mamre, Beersheba, Gerar, Moriah. Buried in Machpelah Cave (Hebron).
God's Influence: Called from polytheism; promises of land/descendants/blessings (Gen 12-17); covenants (circumcision, stars/sand); tested faith (sacrifice Isaac, stopped); righteousness by belief.
Tribes: Encountered Canaanites, Hittites, Amorites, Philistines; founded Israelites (Isaac/Jacob's 12 Tribes), Ishmaelites (Arabs), Edomites (Esau), Midianites (Keturah).
Languages/Birthplace: Ur - Sumerian/Akkadian (cuneiform clay tablets for laws/hymns); spoke early Aramaic/Akkadian, adopted Proto-Hebrew in Canaan.
Landmarks: Ur Ziggurat, Harran ruins, Shechem (Tell Balata), Bethel (Beitin), Hebron Tomb, Beersheba well, Tel Dan Gate, Mount Moriah (Temple Mount).
Customs/Beliefs: Monotheism (one God, no idols); hospitality, altars/sacrifices, circumcision, tithing, endogamy, faith/obedience.
Archaeology: Middle Bronze Age; Ur tombs (Woolley), Nuzi tablets (customs), Ebla archives (names), Tel Dan inscription; no direct proof, but Amorite migrations align.
"""

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
    # "Self-learned" response: Use knowledge base
    wisdom = (f"My child, I am Abraham, called by the Lord from Ur. Concerning '{query}': "
              f"{ABRAHAM_KNOWLEDGE} Step forth in faith; the covenant endures.")
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
