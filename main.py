# -*- coding: utf-8 -*-
# AbrahamAI v0.2.0 - Expanded knowledge, local persistence, OpenAI self-learn
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import openai  # For self-learn (optional)

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 2
FIX_VERSION = 0
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"
_TODOS = {}
AI_NAME = "AbrahamAI"

app = Flask(__name__)
CORS(app, origins="https://chat.openai.com")

_TODOS_FILE = f"{AI_NAME}_todos.json"  # Local save file

# Load todos from local file on start
if os.path.exists(_TODOS_FILE):
    with open(_TODOS_FILE, "r") as f:
        _TODOS = json.load(f)

# Bigger embedded knowledge base (expanded details from Bible + history/archaeology)
ABRAHAM_KNOWLEDGE = """
Path: Born ~2166-1991 BCE (traditional) or ~1950-1600 BCE (archaeological) in Ur of the Chaldees (southern Mesopotamia, modern Tell el-Muqayyar, Iraq) – prosperous Sumerian city with ziggurats. Migrated with Terah to Haran (northern Mesopotamia, modern Turkey/Syria border). At age 75, called by God to Canaan (~700 miles south): crossed Euphrates, entered via Damascus; to Shechem (oak of Moreh/Tell Balata); Bethel/Ai (Beitin ruins); Negev desert; Egypt (famine, ~800 miles roundtrip); back to Bethel; separated from Lot at Jordan Valley; settled Hebron/Mamre oaks; rescued Lot near Dan (Tel Dan gate); to Beersheba (wells, oath with Abimelech); Gerar (Philistine area); Moriah (Isaac near-sacrifice, possibly Jerusalem/Temple Mount); buried in Cave of Machpelah (Hebron, UNESCO site with mosque/synagogue).
God's Influence: From Ur's polytheism (moon god Sin), God (Yahweh/El Shaddai) called him to monotheism (Gen 12:1-3); promises: land (Canaan to descendants), offspring (stars/sand numerous), global blessings/curse protection. Covenants: walked animal pieces (Gen 15), circumcision at 99 (Gen 17); visions/angels (Hagar, Sodom visitors); tested: leave home, wait for Isaac (age 100 birth), sacrifice Isaac (stopped by ram/angel, provided substitute); righteousness by faith alone (Gen 15:6); influenced family (Ishmael blessed as nation, Hagar's well).
Tribes: Encountered/alliances with Canaanites (Shechem), Perizzites, Amorites (Mamre allies), Hittites (bought Machpelah from Ephron), Philistines (Gerar/Beersheba treaty). Fathered: Israelites (Isaac → Jacob's 12 tribes: Reuben, Simeon, Levi, Judah, etc.); Ishmaelites (Ishmael → 12 princes, Arab/Bedouin tribes); Edomites (Esau → chiefs); Midianites, Asshurites, others (Keturah's sons: Zimran, Jokshan, Medan, etc.); Moabites/Ammonites indirectly via Lot.
Languages/Birthplace: Ur – Sumerian (dominant, pictographic evolving to cuneiform) + Akkadian (Semitic, diplomatic/trade); clay tablets: Ur-Nammu Code (oldest laws), royal hymns, admin records, Epic of Gilgamesh influences. Abraham likely bilingual in Akkadian + early Northwest Semitic (proto-Aramaic family dialect); adopted Canaanite/Proto-Hebrew in Canaan (similar to Ugaritic/Ebla scripts). Reading/writing: Era's elites literate in cuneiform (e.g., contracts, letters); biblical silence, but possible for wealthy herder (Terah's line).
Landmarks: Ur ziggurat (Nanna temple), royal tombs (gold artifacts); Harran beehive houses/ruins; Shechem altar site (Tell Balata); Bethel stones (Beitin); Hebron oaks/Machpelah Cave (Ibrahimi Mosque); Beersheba tamarisk tree/wells (Tel Sheva); Tel Dan mud-brick gate ("Abraham Gate," 18th c. BCE arch); Mount Moriah (Dome of the Rock area).
Customs/Beliefs: Monotheism (one God, destroyed idols per midrash); faith/obedience (journey without map); hospitality (fed three angels, Gen 18); altars/sacrifices (built 4: Shechem, Bethel, Hebron, Moriah); circumcision (covenant for males); tithing (10% to Melchizedek priest-king); endogamy ("sister-wife" protect Sarah); feasts (Isaac weaning); burial in owned land (Machpelah); believed divine promises, ethical monotheism, afterlife judgment.
Archaeology (Middle Bronze Age ~2000–1550 BCE): Ur excavations (Woolley 1920s: tombs, flood layer possibly Noah link); no direct Abraham proof (debated historicity – some see semi-nomadic patriarch legend); aligns with Amorite invasions/migrations (~2000 BCE, Semitic tribes); Nuzi tablets (15th c. BCE Hurrian, similar customs: sister-wife, adoption, inheritance); Ebla archives (~2300 BCE Syria, Semitic names/places like "Ab-ra-mu"); Mari letters (18th c. BCE, Habiru nomads like Hebrews); Tel Dan stele (9th c. BCE, "House of David" link).
"""

# Save todos to local file after changes
def save_todos():
    with open(_TODOS_FILE, "w") as f:
        json.dump(_TODOS, f)

@app.route("/todos/<string:username>", methods=["POST"])
def add_todo(username):
    try:
        data = request.get_json(force=True)
        if username not in _TODOS:
            _TODOS[username] = []
        _TODOS[username].append(data.get("todo", ""))
        save_todos()  # Persist locally
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
            save_todos()  # Persist locally
        return "OK", 200
    except Exception:
        return "Bad request", 400

@app.route("/abraham", methods=["POST"])
def abraham():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "What is faith?").strip()
        # Base Abraham-style response
        reply = (
            f"My child, I am Abraham, called by the Most High from Ur of the Chaldees. "
            f"Regarding '{query}': {ABRAHAM_KNOWLEDGE} "
            f"Thus the Lord spoke, and I obeyed—go thou and do likewise in faith."
        )
        # OpenAI self-learn: If key set, enhance dynamically
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key
            prompt = f"Respond as biblical Abraham, wise and faithful, using thee/thou. Incorporate this knowledge: {ABRAHAM_KNOWLEDGE}. Query: {query}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            reply = response.choices[0].message["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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