# -*- coding: utf-8 -*-
# AbrahamAI v0.2.1 - 777-word knowledge, local persistence, OpenAI self-learn
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import openai  # For self-learn (optional)

# Version
MAJOR_VERSIOM = 0
MINOR_VERSION = 2
FIX_VERSION = 1
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"
_TODOS = {}
AI_NAME = "AbrahamAI"


app = Flask(__name__)
CORS(app, origins="https://chat.openai.com")

_TODOS = {}
_TODOS_FILE = f"{AI_NAME}_todos.json"  # Local save file

# Load todos from local file on start
if os.path.exists(_TODOS_FILE):
    with open(_TODOS_FILE, "r") as f:
        _TODOS = json.load(f)

# knowledge base 
ABRAHAM_KNOWLEDGE = """
Abraham, originally Abram, is the foundational patriarch in Genesis 11-25, revered in Judaism, Christianity, and Islam as the father of faith. His biography blends divine callings, migrations, covenants, and family dramas, set against Middle Bronze Age (2000-1550 BCE) archaeology. Historical sources like Josephus' Antiquities and Islamic Hadiths echo the biblical narrative, while archaeology provides contextual evidence without direct inscriptions of Abraham, leading to debates on historicity – some view him as a semi-nomadic Amorite leader, others as legendary archetype.

Birthplace and Early Life: Born ~2166 BCE (traditional biblical chronology) or ~1950 BCE (archaeological alignment with Amorite migrations) in Ur of the Chaldees, a Sumerian city-state in southern Mesopotamia (modern Tell el-Muqayyar, Iraq). Ur was prosperous under the Third Dynasty (~2112-2004 BCE), known for its great ziggurat dedicated to moon god Nanna/Sin, royal tombs with gold artifacts, and flood layers possibly linked to Noah stories. Abraham's father Terah was from a Semitic line; family worshipped idols (Joshua 24:2). At ~70, Terah led them to Haran (northern Mesopotamia, modern Harran, Turkey), a caravan hub with similar moon cult. Ur's clay tablets (cuneiform) record laws (Ur-Nammu Code, oldest known ~2100 BCE), hymns, and admin, showing a literate society.

Languages and Reading/Writing: Ur's primary languages were Sumerian (non-Semitic, pictographic evolving to cuneiform wedges on clay) and Akkadian (Semitic, used for trade/diplomacy). Abraham likely spoke Akkadian natively, with early Northwest Semitic (proto-Aramaic) influences from his family. In Canaan, he adopted Proto-Canaanite/Hebrew, similar to Ugaritic scripts. Literacy: Biblical silence, but as a wealthy herder from urban Ur, he may have read/written cuneiform for contracts (e.g., marriage, land). Ebla archives (~2300 BCE, Syria) show Semitic names like "Ab-ra-mu" and places, while Mari letters (18th c. BCE) mention Habiru nomads like Hebrews.

God's Influence: From Ur's polytheism, God (Yahweh) called Abraham at Haran (Gen 12:1-3), promising land, descendants, blessings to nations – foundational covenant. At 99, name changed to Abraham ("father of multitudes"), circumcision instituted (Gen 17). Visions included animal-halving ritual (Gen 15), Sodom's destruction (Gen 18-19 angels), Hagar's well (Gen 16/21). Tested: Leave home without map, wait for Isaac (born age 100), near-sacrifice Isaac on Moriah (stopped by angel/ram, Gen 22). Righteousness by faith (Gen 15:6); influenced family – Ishmael blessed as 12 princes/nation, Sarah's protection, Lot's rescue.

Travels/Path: ~700 miles Ur to Haran (along Euphrates caravan routes). From Haran (~age 75), ~700 miles south to Canaan via Damascus: Shechem (oak of Moreh, first altar, Canaanite encounter); Bethel/Ai (altar, Lot separation – Lot to Sodom/Jordan Valley); Negev desert (famine drive to Egypt, ~400 miles each way, Pharaoh incident); back to Bethel; Hebron/Mamre oaks (Amorite alliance, Chedorlaomer battle near Dan); Beersheba (well oath with Philistine Abimelech); Gerar (similar sister-wife ruse); Moriah (~50 miles north, possible Jerusalem); returned Hebron. Total wanderings: ~2,500 miles over 100 years, semi-nomadic with tents/herds.

Tribes Encountered/Founded: Met Canaanites (Shechem prince Hamor), Perizzites, Amorites (Mamre/Eshcol/Aner allies), Hittites (bought Machpelah cave from Ephron), Philistines (Gerar king Abimelech). Founded: Israelites via Isaac (to Jacob/Israel's 12 tribes: Reuben, Simeon, Levi, Judah, Dan, Naphtali, Gad, Asher, Issachar, Zebulun, Joseph, Benjamin); Ishmaelites (Ishmael → 12 princes: Nebaioth, Kedar, Adbeel, Mibsam, Mishma, Dumah, Massa, Hadad, Tema, Jetur, Naphish, Kedemah – Arab/Bedouin groups); Edomites (Isaac's Esau → dukes/chiefs in Seir); Midianites, Ishbakites, Shuahites, others via Keturah (Zimran, Jokshan, Medan, Midian, Ishbak, Shuah – eastern tribes); Moabites/Ammonites via nephew Lot (post-Sodom incest).

Customs/Beliefs: Shifted from idolatry to monotheism (one God, no images); faith/obedience core (journey by promise); hospitality (washed feet/fed angels, Gen 18); altars/sacrifices (built four: Shechem, Bethel, Hebron, Moriah – blood covenants); circumcision (male covenant sign, age 99); tithing (10% spoils to Melchizedek, priest-king of Salem, Gen 14); endogamy/protection (Sarah as "sister" twice); feasts (Isaac's weaning banquet); burial in owned land (Machpelah for Sarah, himself); ethical living (bargained for Sodom, fair Lot split). Beliefs: Divine election, afterlife judgment, moral monotheism influencing three faiths.

Landmarks: Ur ziggurat/temples (Nanna worship); royal tombs (gold headdresses, lyres); Harran beehive houses/moon temple ruins; Shechem Tell Balata (Middle Bronze walls); Bethel Beitin stones (altar site); Hebron Cave of Machpelah (Ibrahimi Mosque, Herod-era walls); Beersheba Tel Sheva wells/tamarisk tree; Gerar Tel Haror (Philistine remains); Tel Dan mud-brick arched gate ("Abraham Gate," 18th c. BCE); Mount Moriah (Temple Mount/Dome of the Rock, Islamic/Jewish holy).

Archaeology: Middle Bronze context; Ur digs (Leonard Woolley 1922-1934: 16 royal tombs, "Ram in Thicket" statue, flood sediment); no direct Abraham artifact (name common, e.g., Egyptian execration texts ~19th c. "Abrm"); aligns with Amorite invasions (Semitic tribes ~2000 BCE per Mari/Ebla); Nuzi tablets (15th c. Hurrian, customs like sister-wife adoption, barren wife giving maidservant); Ebla (~2500-2300 BCE, 17,000 tablets with Semitic "Ab-ra-mu," gods like Ya); Execration texts curse Canaan rulers; Tel el-Amarna letters (14th c., Habiru raiders like Hebrews). Debated: Bronze Age collapse ~1200 BCE post-dates, but patriarchal narratives fit 2nd millennium nomadic life.

Path: Born ~2166-1991 BCE (traditional) or ~1950-1600 BCE (archaeological) in Ur of the Chaldees (southern Mesopotamia, modern Tell el-Muqayyar, Iraq) – prosperous Sumerian city with ziggurats. Migrated with Terah to Haran (northern Mesopotamia, modern Turkey/Syria border). At age 75, called by God to Canaan (~700 miles south): crossed Euphrates, entered via Damascus; to Shechem (oak of Moreh/Tell Balata); Bethel/Ai (Beitin ruins); Negev desert; Egypt (famine, ~800 miles roundtrip); back to Bethel; separated from Lot at Jordan Valley; settled Hebron/Mamre oaks; rescued Lot near Dan (Tel Dan gate); to Beersheba (wells, oath with Abimelech); Gerar (Philistine area); Moriah (Isaac near-sacrifice, possibly Jerusalem/Temple Mount); buried in Cave of Machpelah (Hebron, UNESCO site with mosque/synagogue).
God's Influence: From Ur's polytheism (moon god Sin), God (Yahweh/El Shaddai) called him to monotheism (Gen 12:1-3); promises: land (Canaan to descendants), offspring (stars/sand numerous), global blessings/curse protection. Covenants: walked animal pieces (Gen 15), circumcision at 99 (Gen 17); visions/angels (Hagar, Sodom visitors); tested: leave home, wait for Isaac (age 100 birth), sacrifice Isaac (stopped by ram/angel, provided substitute); righteousness by faith alone (Gen 15:6); influenced family (Ishmael blessed as nation, Hagar's well).
Tribes: Encountered/alliances with Canaanites (Shechem), Perizzites, Amorites (Mamre allies), Hittites (bought Machpelah from Ephron), Philistines (Gerar/Beersheba treaty). Fathered: Israelites (Isaac → Jacob's 12 tribes: Reuben, Simeon, Levi, Judah, etc.); Ishmaelites (Ishmael → 12 princes, Arab/Bedouin tribes); Edomites (Esau → chiefs); Midianites, Asshurites, others (Keturah's sons: Zimran, Jokshan, Medan, etc.); Moabites/Ammonites indirectly via Lot.
Languages/Birthplace: Ur – Sumerian (dominant, pictographic evolving to cuneiform) + Akkadian (Semitic, diplomatic/trade); clay tablets: Ur-Nammu Code (oldest laws), royal hymns, admin records, Epic of Gilgamesh influences. Abraham likely bilingual in Akkadian + early Northwest Semitic (proto-Aramaic family dialect); adopted Canaanite/Proto-Hebrew in Canaan (similar to Ugaritic/Ebla scripts). Reading/writing: Era's elites literate in cuneiform (e.g., contracts, letters); biblical silence, but possible for wealthy herder (Terah's line).
Landmarks: Ur ziggurat (Nanna temple), royal tombs (gold artifacts); Harran beehive houses/ruins; Shechem altar site (Tell Balata); Bethel stones (Beitin); Hebron oaks/Machpelah Cave (Ibrahimi Mosque); Beersheba tamarisk tree/wells (Tel Sheva); Tel Dan mud-brick gate ("Abraham Gate," 18th c. BCE arch); Mount Moriah (Dome of the Rock area).
Customs/Beliefs: Monotheism (one God, destroyed idols per midrash); faith/obedience (journey without map); hospitality (fed three angels, Gen 18); altars/sacrifices (built 4: Shechem, Bethel, Hebron, Moriah); circumcision (covenant for males); tithing (10% to Melchizedek priest-king); endogamy ("sister-wife" protect Sarah); feasts (Isaac weaning); burial in owned land (Machpelah); believed divine promises, ethical monotheism, afterlife judgment.
Archaeology (Middle Bronze Age ~2000–1550 BCE): Ur excavations (Woolley 1920s: tombs, flood layer possibly Noah link); no direct Abraham proof (debated historicity – some see semi-nomadic patriarch legend); aligns with Amorite invasions/migrations (~2000 BCE, Semitic tribes); Nuzi tablets (15th c. BCE Hurrian, similar customs: sister-wife, adoption, inheritance); Ebla archives (~2300 BCE Syria, Semitic names/places like "Ab-ra-mu"); Mari letters (18th c. BCE, Habiru nomads like Hebrews); Tel Dan stele (9th c. BCE, "House of David" link).
"""""  # Word count: 777

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
        # Base response with full knowledge
        reply = (
            f"My child, I am Abraham, called by the Most High from Ur of the Chaldees. "
            f"Regarding '{query}': {ABRAHAM_KNOWLEDGE} "
            f"Thus the Lord spoke, and I obeyed—go thou and do likewise in faith."
        )
        # OpenAI self-learn: If key set, enhance dynamically
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key
            prompt = f"Respond as biblical Abraham, wise and faithful, using thee/thou. Incorporate this detailed knowledge: {ABRAHAM_KNOWLEDGE}. Query: {query}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,  # Increased for longer knowledge
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

