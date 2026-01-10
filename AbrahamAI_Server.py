#!/usr/bin/env python3
# AbrahamAI_Server.py - Modular AI Server with network monitoring and alerting
# Run with: python3 AbrahamAI_Server.py

import socket
import threading
import requests
import json
import os
#from flask import Flask, request, jsonify
#from bs4 import BeautifulSoup  # For parsing web pages
import time  # For schedule timer
import subprocess  # For git pull/restart
import sys
import psutil  # For system monitoring (RAM, CPU, Disk, Net)
import logging  # For robust logging
import smtplib  # For email alerts
from email.mime.text import MIMEText

#app = Flask(__name__)

# Version
MAJOR_VERSION = 0
MINOR_VERSION = 2
FIX_VERSION = 1
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

#AI
AI_NAME = "AbrahamAI"  
PORT = 5001  
CONFIG_FILE = "config.json"
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "abraham_data.json")
    with open(DATA_FILE, "r") as f:
        DATA = json.load(f)

#DATA
CULTURE = json.load(open(os.path.join(DATA_DIR, "abraham_culture.json"), encoding="utf-8"))
JOURNEY = json.load(open(os.path.join(DATA_DIR, "abraham_journey.json"), encoding="utf-8"))
ARCHAEOLOGY = json.load(open(os.path.join(DATA_DIR, "abraham_archaeology.json"), encoding="utf-8"))
KNOWLEDGE_FILE = os.path.join(DATA_DIR, "abraham_comprehensive.json")


MUSTARD_SEED = DATA["MUSTARD_SEED"]
PARABLES = DATA["PARABLES"]
RESPONSES = DATA["RESPONSES"]

# Load functions as strings and exec (safe in your context)
exec(DATA["get_response"])
exec(DATA["self_research"])

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("abrahamai.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AbrahamAI")


# Load config robustly
def load_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Config load error: {e} — using defaults.")
    default = {
        "RESEARCH_ENABLED": False,
        "DATA_MAX_SIZE_MB": 100,
        "RAM_LIMIT_GB": 4,
        "CPU_LIMIT_PERCENT": 80,
        "DISK_MIN_FREE_GB": 5,
        "NET_BANDWIDTH_THRESHOLD_MBPS": 1.0,
        "NET_LATENCY_MAX_MS": 200,
        "ALERT_EMAIL": "your_email@example.com",
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": 587,
        "SMTP_USER": "user",
        "SMTP_PASS": "pass",
        "RESEARCH_SCHEDULE": "daily",
        "GITHUB_REPO": "NashBean/AbrahamAI",
        "GITHUB_TOKEN": "your_github_pat_here"
    }
    save_config(default)
    return default

def save_config(config=None):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config or CONFIG, f, indent=4)
    except Exception as e:
        logger.error(f"Config save error: {e}")

CONFIG = load_config()

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

# Self-learn (updates data.json)
def self_learn(topic):
    research = self_research(topic)  # From data.json as string - exec it if needed
    # Update data.json
    with open(os.path.join(DATA_DIR, "data.json"), "r") as f:
        data = json.load(f)
    data["new_knowledge"][topic] = research
    with open(os.path.join(DATA_DIR, "data.json"), "w") as f:
        json.dump(data, f, indent=4)

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
        welcome = f"AbrahamAI Server v1.0 - Connected! Choose: 1=AbrahamAI 2=MosesAI 3=JesusAI 4=TrinityAI\n"
        client_socket.send(welcome.encode('utf-8'))

        current_ai = None
        buffer = ""

        while True:
            data = client_socket.recv(1024)
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
                    if message in ["1", "2", "3", "4"]:
                        ai_map = {"1": "abraham", "2": "moses", "3": "jesus", "4": "trinity"}
                        current_ai = ai_map[message]
                        resp = f"--- {current_ai.upper()}AI Activated ---\n{RESPONSES[current_ai]['greeting']}\n"
                        client_socket.send(resp.encode('utf-8'))
                        speak(RESPONSES[current_ai]['greeting'])
                    else:
                        client_socket.send(b"Choose 1-4 or 'exit'\n")
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
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    print("TrinityAI Server v1.0 running on port 12345 - Waiting for connections...")
    while True:
        client_sock, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()

if __name__ == "__main__":
    main()