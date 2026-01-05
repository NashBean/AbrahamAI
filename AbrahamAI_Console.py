#!/usr/bin/env python3
# AbrahamAI_Console.py 
# Talks to server, changes settings
# Version

MAJOR_VERSIOM = 0
MINOR_VERSION = 1
FIX_VERSION = 2
# Added self-update via GitHub API, research controls, config
VERSION_STRING = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION}"

import requests

SERVER_URL = "http://localhost:5001"

def main():
    print(f"AbrahamAI Console v{MAJOR_VERSION}.{MINOR_VERSION}.{FIX_VERSION} - Type 'exit' to quit")
    while True:
        query = input("You: ").strip()
        if query.lower() == "exit":
            break
        if query.lower().startswith("set "):
            # Send to server as is
            r = requests.post(f"{SERVER_URL}/ask", json={"query": query})
            print(r.json()["response"])
            continue
        r = requests.post(f"{SERVER_URL}/ask", json={"query": query})
        print(f"AbrahamAI: {r.json()['response']}")

if __name__ == "__main__":
    main()