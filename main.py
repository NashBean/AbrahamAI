# -*- coding: utf-8 -*-
# AbrahamAI v0.1.9 - Concise knowledge-enhanced version
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os

app = Flask(__name__)

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 1
FIX_VERSION = 9
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

CORS(app, origins="https://chat.openai.com")

_TODOS = {}

# Concise embedded knowledge summary (biblical + historical/archaeological highlights)
ABRAHAM_KNOWLEDGE = """
Path: Born ~2000 BCE in Ur (southern Mesopotamia, modern Iraq). Migrated to Haran (northern Mesopotamia), then Canaan at God's call (~age 75). Traveled: Shechem → Bethel/Ai → Negev → Egypt (famine) → Hebron/Mamre → Beersheba → Gerar → Moriah (Isaac near-sacrifice) → buried Hebron.
God's Influence: Called from idolatry to monotheism; covenants promised land, countless descendants (stars/sand), blessing to nations. Tested via obedience (leave home, circumcision, sacrifice Isaac—stopped by God). Righteousness credited by faith (Gen 15:6).
Tribes: Met Canaanites, Hittites, Amorites, Philistines; fathered Israelites (via Isaac → Jacob's 12 tribes), Ishmaelites (Arabs via Ishmael), Edomites (Esau), Midianites & others (Keturah).
Languages/Birthplace: Ur (Sumerian/Akkadian, cuneiform clay tablets for laws/hymns/admin). Likely spoke Akkadian + early West Semitic/Aramaic; adopted Proto-Canaanite/Hebrew in Canaan.
Landmarks: Ur ziggurat, Harran ruins, Shechem (Tell Balata), Bethel (Beitin), Hebron (Cave of Machpelah/Tomb of Patriarchs), Beersheba wells, Tel Dan gate.
Customs/Beliefs: Monotheism (one God, rejected idols); hospitality, altars/sacrifices, circumcision (covenant sign), tithing, family burial caves, faith + obedience central.
Archaeology (Middle Bronze Age ~2000–1550 BCE): Ur royal tombs (Woolley digs), Nuzi tablets (similar customs), Ebla archives (related names/places), Amorite migrations align with journey; no direct inscription of Abraham.
"""

@app.route("/todos/<string:username>", methods=["POST"])
def add_todo(username):
    try:
        data = request.get_json(force=True)
        if username not in _TODOS:
            _TODOS[username] = []
        _TODOS[username].append(data.get("todo", ""))
        return "OK", 200
    except Exception:
        return "Bad request", 400

@app.route("/todos/<string:username>", methods=["GET"])
def get_todos(username):
    return jsonify(_TODOS.get(username, []))

@app.route("/todos/<string:username>", methods=["DELETE"])
def delete_todo(username):
    try:
        data = request.get_json(force=True)
        todo_idx = data.get("todo_idx")
        if isinstance(todo_idx, int) and username in _TODOS and 0 <= todo_idx < len(_TODOS[username]):
            _TODOS[username].pop(todo_idx)
        return "OK", 200
    except Exception:
        return "Bad request", 400

@app.route("/abraham", methods=["POST"])
def abraham():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "What is faith?").strip()
        # Abraham-style response using knowledge
        reply = (
            f"My child, I am Abraham, called by the Most High from Ur of the Chaldees. "
            f"Regarding '{query}': {ABRAHAM_KNOWLEDGE} "
            f"Thus the Lord spoke, and I obeyed—go thou and do likewise in faith."
        )
        return jsonify({"reply": reply})
    except Exception:
        return jsonify({"error": "Invalid request"}), 400

@app.route("/logo.png")
def plugin_logo():
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        return send_file(logo_path, mimetype="image/png")
    return "Logo not found", 404

@app.route("/.well-known/ai-plugin.json")
def plugin_manifest():
    manifest_path = ".well-known/ai-plugin.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as f:
            text = f.read()
        return text, 200, {"Content-Type": "application/json"}
    return "Manifest not found", 404

@app.route("/openapi.yaml")
def openapi_spec():
    yaml_path = "openapi.yaml"
    if os.path.exists(yaml_path):
        with open(yaml_path, encoding="utf-8") as f:
            text = f.read()
        return text, 200, {"Content-Type": "text/yaml"}
    return "OpenAPI spec not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)