#!/usr/bin/env python3
import re
import requests
import json

from collections import defaultdict
from thefuzz import fuzz

WIKIDATA_API = "https://www.wikidata.org/w/api.php"

HEADERS = {
    # Replace with your app name and email or website
    "User-Agent": "WikidataExistenceChecker/1.0 (contact: mbalazs215@gmail.com)"
}

def wikidata_entity_exists(entity_id: str, entity_name: str) -> bool:
    entity_id = entity_id.strip().upper()

    if not re.fullmatch(r"[QP]\d+", entity_id):
        raise ValueError("Wikidata ID must look like Q123 or P123")

    params = {
        "action": "wbgetentities",
        "ids": entity_id,
        "props": "info|labels",
        "format": "json",
        "languages": "en",
    }

    response = requests.get(
        WIKIDATA_API,
        params=params,
        headers=HEADERS,
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    print(data)
    entity = data.get("entities", {}).get(entity_id)

    try:
        actual_name = "_".join(entity['labels']['en']['value'].lower().split(" "))
    except KeyError:
        return False

    return entity is not None and "missing" not in entity and fuzz.ratio(actual_name, entity_name) > 98


def validate(data: dict) -> list:
    halu = list()
    found_cash = set()
    for d in data:
        for u in d["Unary"]:
            for key, content in u.items():
                if content[0] in found_cash and not wikidata_entity_exists(content[0], key):
                    halu.append(content[0])
                else:
                    found_cash.add(content[0])
    return halu

if __name__ == "__main__":
    with open('res_should.json', 'r', encoding='utf8') as fp:
        should = json.load(fp)
    
    with open('res_may.json', 'r', encoding='utf8') as fp:
        may = json.load(fp)
    
    missed_total = dict()
    missed_total['should'] = validate(should)
    missed_total['may'] = validate(may)
    with open('halucinations.json', 'w', encoding='utf8') as fp:
        json.dump(missed_total, fp, indent=1)
    