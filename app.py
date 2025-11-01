import os
from flask import Flask, request, jsonify, Response
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# YOUR FINE-TUNED MODEL (English base)
EN_MODEL = "ft:gpt-4o-mini:personal:abraham_v4:abc123"

# MULTILINGUAL PROMPTS
HEBREW_SYSTEM = """
אתה אברהם אבינו מדבר עברית מקראית תקנית. 
דבר בסגנון בראשית יב-כה, השתמש בלשון קדומה: 
הִנֵּה, כִּי, אֲדֹנָי, בְּרִית, זֹאת, וַיֹּאמֶר.
התייחס למיתוסים אוגריתיים, חתיים, מסופוטמיים – וקשר תמיד לחיי ולברית עם ה'.
"""

ARAMAIC_SYSTEM = """
אתה אברהם אבינו מדבר ארמית תלמודית/מקראית. 
השתמש בלשון דניאל/עזרא: דִּי, לָא, מַלְכוּתָא, קֳדָם.
קשר מיתוסים עתיקים לחיי ולברית עם אל שדי.
"""

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json.get('query', '')
    response = client.chat.completions.create(
        model=EN_MODEL,
        messages=[
            {"role": "system", "content": "You are Abraham from Genesis. Speak in archaic English."},
            {"role": "user", "content": query}
        ],
        max_tokens=300
    )
    return jsonify({"response": response.choices[0].message.content})

# ——— HEBREW MODE ———
@app.route('/hebrew', methods=['POST'])
def hebrew():
    query = request.json.get('query', '')
    
    # Generate Hebrew response
    response = client.chat.completions.create(
        model=EN_MODEL,
        messages=[
            {"role": "system", "content": HEBREW_SYSTEM},
            {"role": "user", "content": query}
        ],
        max_tokens=300
    )
    hebrew_text = response.choices[0].message.content

    # Generate Hebrew audio (TTS with Hebrew voice)
    speech = client.audio.speech.create(
        model="tts-1",
        voice="onyx",  # Deep male voice (works with Hebrew)
        input=hebrew_text
    )

    return Response(
        speech.content,
        mimetype="audio/mpeg",
        headers={"Content-Disposition": "attachment;filename=abraham_hebrew.mp3"}
    )

# ——— ARAMAIC MODE ———
@app.route('/aramaic', methods=['POST'])
def aramaic():
    query = request.json.get('query', '')
    
    # Generate Aramaic response
    response = client.chat.completions.create(
        model=EN_MODEL,
        messages=[
            {"role": "system", "content": ARAMAIC_SYSTEM},
            {"role": "user", "content": query}
        ],
        max_tokens=300
    )
    aramaic_text = response.choices[0].message.content

    # Generate Aramaic audio
    speech = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=aramaic_text
    )

    return Response(
        speech.content,
        mimetype="audio/mpeg",
        headers={"Content-Disposition": "attachment;filename=abraham_aramaic.mp3"}
    )

# ——— ENGLISH SPEAK (existing) ———
@app.route('/speak', methods=['POST'])
def speak():
    query = request.json.get('query', '')
    response = client.chat.completions.create(
        model=EN_MODEL,
        messages=[
            {"role": "system", "content": "You are Abraham. Speak in archaic English."},
            {"role": "user", "content": query}
        ],
        max_tokens=300
    )
    text = response.choices[0].message.content
    speech = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    return Response(speech.content, mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)