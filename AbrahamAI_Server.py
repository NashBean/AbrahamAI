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
FIX_VERSION = 0
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

#AI
AI_NAME = "AbrahamAI"  
PORT = 5001  
DATA_DIR = "data"
CONFIG_FILE = "config.json"

#DATA
CULTURE = json.load(open(os.path.join(DATA_DIR, "abraham_culture.json"), encoding="utf-8"))
JOURNEY = json.load(open(os.path.join(DATA_DIR, "abraham_journey.json"), encoding="utf-8"))
ARCHAEOLOGY = json.load(open(os.path.join(DATA_DIR, "abraham_archaeology.json"), encoding="utf-8"))
KNOWLEDGE_FILE = os.path.join(DATA_DIR, "abraham_comprehensive.json")


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

# Core Mustard Seed
MUSTARD_SEED = (
    "Matthew 13:31-32 (KJV): Another parable put he forth unto them, saying, The kingdom of heaven is like to a grain of mustard seed, "
    "which a man took, and sowed in his field: Which indeed is the least of all seeds: but when it is grown, it is the greatest among herbs, "
    "and becometh a tree, so that the birds of the air come and lodge in the branches thereof."
)

# Expanded Parables Dict (completed from your code)
PARABLES = {
    "lamp on a stand": {
        "references": "Matthew 5:14-16; Mark 4:21-22; Luke 8:16",
        "verses": "Matthew 5:14-16 (KJV): Ye are the light of the world. A city that is set on an hill cannot be hid. Neither do men light a candle, and put it under a bushel, but on a candlestick; and it giveth light unto all that are in the house. Let your light so shine before men, that they may see your good works, and glorify your Father which is in heaven. Mark 4:21-22 (KJV): And he said unto them, Is a candle brought to be put under a bushel, or under a bed? and not to be set on a candlestick? For there is nothing hid, which shall not be manifested; neither was any thing kept secret, but that it should come abroad. Luke 8:16 (KJV): No man, when he hath lighted a candle, covereth it with a vessel, or putteth it under a bed; but setteth it on a candlestick, that they which enter in may see the light."
    },
    "wise and foolish builders": {
        "references": "Matthew 7:24-27; Luke 6:47-49",
        "verses": "Matthew 7:24-27 (KJV): Therefore whosoever heareth these sayings of mine, and doeth them, I will liken him unto a wise man, which built his house upon a rock: And the rain descended, and the floods came, and the winds blew, and beat upon that house; and it fell not: for it was founded upon a rock. And every one that heareth these sayings of mine, and doeth them not, shall be likened unto a foolish man, which built his house upon the sand: And the rain descended, and the floods came, and the winds blew, and beat upon that house; and it fell: and great was the fall of it. Luke 6:47-49 (KJV): Whosoever cometh to me, and heareth my sayings, and doeth them, I will shew you to whom he is like: He is like a man which built an house, and digged deep, and laid the foundation on a rock: and when the flood arose, the stream beat vehemently upon that house, and could not shake it: for it was founded upon a rock. But he that heareth, and doeth not, is like a man that without a foundation built an house upon the earth; against which the stream did beat vehemently, and immediately it fell; and the ruin of that house was great."
    },
    # ... add the rest of your PARABLES dict from your original code ...
}

# Responses
RESPONSES = {
    "abraham": {
        "greeting": "I am AbrahamAI — called by the Father, father of faith and many nations.",
        "faith": f"Genesis 15:5-6 (KJV): And he believed in the LORD; and he counted it to him for righteousness.\n\nSmall faith grows like the mustard seed into eternal promise. {MUSTARD_SEED}",
        "sabbath": "Genesis 2:2-3 (KJV): And on the seventh day God ended his work which he had made; and he rested on the seventh day from all his work which he had made. And God blessed the seventh day, and sanctified it: because that in it he had rested from all his work which God created and made.\n\nThe Father established the seventh day as holy from creation.",
        "default": "Genesis 22:18 (KJV): And in thy seed shall all the nations of the earth be blessed; because thou hast obeyed my voice.\n\nWhat promise is the Father speaking to you today?"
    }
    # ... add full RESPONSES for other AIs if needed ...
}

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