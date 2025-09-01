import os

HOST = os.getenv("HOST", "127.0.0.1")
INDEX_NAME = os.getenv("INDEX_NAME", "malicious_text_test")

MAPPINGS = {"properties":{
    "CreateDate": {"type": "keyword"},
    "Antisemitic": {"type": "integer"},
    "text": {"type": "text"},
    "sentiment": {"type": "keyword"},
    "weapons_detected": {"type": "text"}
}}

WEAPONS_PATH = 'data/weapon_list.txt'
TWEETS_PATH = 'data/tweets_injected.csv'