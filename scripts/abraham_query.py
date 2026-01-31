#!/usr/bin/env python3
from bdh_stub import generate_text
import json
import argparse

MAJOR_VERSION = 0
MINOR_VERSION = 2
FIX_VERSION = 0

def load_knowledge():
    with open("data/abraham_knowledge.json", "r") as f:
        return json.load(f)

def query_abraham(question):
    knowledge = load_knowledge()
    prompt = f"""You are AbrahamAI, a reverent assistant helping people understand the Biblical prophet Abraham.
Base every answer first on Scripture. Use historical and archaeological information only as supporting context.
Never contradict the Bible. Be humble and truthful.

Knowledge base summary: {json.dumps(knowledge, indent=2)}

Question: {question}

Answer:"""
    return generate_text(prompt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question", help="Ask about Abraham")
    args = parser.parse_args()
    print(query_abraham(args.question))