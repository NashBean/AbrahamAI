#!/usr/bin/env python3
# AbrahamAI_Server.py - Modular AI Server with network monitoring and alerting
# Run with: python3 AbrahamAI_Server.py

import socket
import threading
import requests
import json
import os
import time  # For schedule timer
import subprocess  # For git pull/restart
import sys
import psutil  # For system monitoring (RAM, CPU, Disk, Net)
import logging  # For robust logging
import smtplib  # For email alerts

# Import shared from ai-lib (your submodule)
from ai_lib.CommonAI import (
    get_version, 
    load_config, # save_config,
    setup_logging, logger,
    load_data, update_data, send_alert,
    check_system_limits,  
    self_research, self_update,
    understand_language, get_culture, speak,
    get_response
    )

# Version
MAJOR_VERSION = 0
MINOR_VERSION = 2
FIX_VERSION = 9
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

#AI
AI_NAME = "AbrahamAI"  
PORT = 5001  # AbrahamAI port
CONFIG_FILE = "abraham_config.json"
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "abraham_data.json")

VOICE_ON = True

CONFIG = load_config()
logger = setup_logging(CONFIG)
logger.info(f"{AI_NAME} Server {VERSION_STRING} starting...")


#DATA
CULTURE = json.load(open(os.path.join(DATA_DIR, "abraham_culture.json"), encoding="utf-8"))
JOURNEY = json.load(open(os.path.join(DATA_DIR, "abraham_journey.json"), encoding="utf-8"))
ARCHAEOLOGY = json.load(open(os.path.join(DATA_DIR, "abraham_archaeology.json"), encoding="utf-8"))
KNOWLEDGE_FILE = os.path.join(DATA_DIR, "abraham_comprehensive.json")


MUSTARD_SEED = DATA["MUSTARD_SEED"]
PARABLES = DATA["PARABLES"]
RESPONSES = DATA["RESPONSES"]

data = load_data()
response = get_response(data, query)

# Load functions as strings and exec (safe in your context)
exec(DATA["get_responsesexec(DATA["self_research"])


    
# Data dir and knowledge file
os.makedirs(DATA_DIR, exist_ok=True)

# Load knowledge robustly
def load_knowledge():
    try:
        if os.path.exists(KNOWLEDGE_FILE):
            size_mb = os.path.getsize(KNOWLEDGE_FILE) / (1024 * 1024)
            if size_mb > CONFIG["DATA_MAX_SIZE_MB"]:
                logger.warning("Data size exceeded — skipping load.")
                send_alert("Data size limit exceeded")
                return {}
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Knowledge load error: {e}")
        send_alert("Knowledge load failed")
    return {}

KNOWLEDGE = load_knowledge()

# Self-learn (updates {AI_Name}_data.json)
def self_learn(topic):
    if not CONFIG.get("RESEARCH_ENABLED", False):
        return "Self-learn disabled."
    if not check_system_limits(CONFIG):
        return "System limits reached — operation skipped."
    research = self_research(topic)  
    update_data({"learned": {topic: research}}, DATA_FILE)  # From ai-lib
    global KNOWLEDGE
    KNOWLEDGE = load_data(DATA_FILE)  # Reload
    logger.info(f"Self-learned: {topic}")
    return f"Learned '{topic}': {research[:200]}..."  # Truncate for response


# Net research
def research_topic(topic):
    if not CONFIG["RESEARCH_ENABLED"]:
        return "Research disabled."
    if not check_system_limits():
        return "System limits reached — research skipped."
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&titles={topic.replace(' ', '_')}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        pages = data["query"]["pages"]
        page_id = list(pages.keys())[0]
        if page_id != "-1":
            return pages[page_id]["extract"]
        return "No research found."
    except Exception as e:
        logger.error(f"Research error: {e}")
        return f"Research failed: {e}"

# Voice function
def speak(text):
    clean = text.replace('\n', ' ').replace('"', '\\"').replace("'", "\\'")
    os.system(f'espeak "{clean}" 2>/dev/null &')

# Use shared from ai-lib
def get_response(query):
    return get_response(query)  # Calls ai-lib's get_response

# Your get_ai_response
def get_ai_response(user_input):
    text = user_input.lower()
    # Voice toggle
    global VOICE_ON
    if "voice on" in text:
        VOICE_ON = True
        return "Voice output enabled."
    if "voice off" in text:
        VOICE_ON = False
        return "Voice output disabled."
    # Parable detection
    for parable_name in PARABLES:
        if parable_name in text:
            p = PARABLES[parable_name]
            return f"Parable of {parable_name.capitalize()} - {p['references']}\n\nFull Verses: {p['verses']}\n\nThe Father's wisdom revealed through the Son, empowered by the Spirit."
    # Other keywords
    if any(word in text for word in ["faith", "mustard", "seed", "believ"]):
        return RESPONSES.get("faith", RESPONSES["default"])
    if any(word in text for word in ["sabbath", "sabath", "holy day", "seventh day", "rest day", "keep holy", "saturday"]):
        return RESPONSES.get("sabbath", RESPONSES["default"])
    if any(word in text for word in ["sower", "seeds", "soil", "path", "rock", "thorn"]):
        return RESPONSES.get("sower", RESPONSES["default"])
    if "parable" in text:
        return RESPONSES.get("parable", RESPONSES["default"])
    if any(word in text for word in ["fulfill", "prophecy", "law and prophets", "messiah"]):
        return RESPONSES.get("fulfill", RESPONSES["default"])
    return RESPONSES["default"]

# Handle client
def handle_client(client_socket, addr):
    print(f"Connection from {addr}")
    try:
        welcome = f"AbrahamAI Server {VERSION_STRING} \n"
        client_socket.send(welcome.encode('utf-8'))

        current_ai = None
        buffer = ""

        while True:
            data = client_socket.recv(1024)# Import shared from ai-lib (your submodule)
            if not data:
                break
            buffer += data.decode('utf-8', errors='ignore')

            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                message = line.strip()
                if not message:
                    continue
                if message.lower() == "exit":
                    client_socket.send(b"Grace and peace - until next time!\n")
                    return

                if current_ai is None:
                    if message.lower().startswith("learn "):
                        topic = message[6:].strip()
                        resp = self_learn(topic)
                        full_resp = f"{current_ai.upper()}AI: {resp}\n"
                        client_socket.send(full_resp.encode('utf-8'))
                        speak(resp)
                        continue
                response = get_ai_response(message)
                full_resp = f"{current_ai.upper()}AI: {response}\n"
                client_socket.send(full_resp.encode('utf-8'))
                speak(response)
    except:
        pass
    finally:
        client_socket.close()
        print(f"Disconnected: {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", PORT))
    server.listen(5)
    print(f"{AI_NAME} Server {VERSION_STRING} running on port {PORT}...")
    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()

if __name__ == "__main__":
    main()