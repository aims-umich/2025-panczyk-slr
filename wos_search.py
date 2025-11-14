import requests
import os
from dotenv import load_dotenv
import itertools
from tqdm import tqdm
import pandas as pd
import json


def get_search_combos():
    population_terms = [
        "nuclear",
        "aerospace",
        # "health*",
        # "medic*",
        # "clinical",
        # "autonomous driving",
        # "transportation",
        # "construction",
        # "cars",
        # "engineering",
        # "energy",
        # "sensitive industry",
    ]
    interv_terms_ai = [
        "artifical intelligence",
        "machine learning",
        # "neural networks",
        # "language models",
    ]
    interv_terms_decision = ["decision*"]
    outcome_terms = [
        "incidents",
        "accidents",
        # "near misses",
        # "injuries",
        # "failures",
        # "adverse event",
    ]
    combinations = list(
        itertools.product(
            population_terms, interv_terms_ai, interv_terms_decision, outcome_terms
        )
    )
    return combinations


def generate(api_key, combinations):
    headers = {"X-ApiKey": api_key}
    url = "https://api.clarivate.com/apis/wos-starter/v1/documents"
    frames = []
    for pop, interv_ai, interv_dm, outcome in tqdm(combinations):
        params = {
            "db": "WOS",
            "q": f"TS=({pop}) AND TS=({interv_ai} NEAR/5 {interv_dm}) AND TS=({outcome}) AND PY=2015-2026 AND DT=(Article)",
            "limit": 10,
            "page": 1,
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()["hits"]
        print(type(data))
        if len(data) > 1:
            df = pd.json_normalize(data)
            frames.append(df)
            continue
    result = pd.concat(frames, ignore_index=True, sort=False)
    result["names.authors"] = result["names.authors"].apply(cleanup_authors)
    useful_columns = list(column_map.keys())
    print(result.columns)
    print(useful_columns)
    result = result[useful_columns]
    result.to_csv("search_results/wos_searches.csv")


# "[{'displayName': 'Kegyes, Tamas', 'wosStandard': 'Kegyes, T', 'researcherId': 'DWO-9473-2022'}, {'displayName': 'Sule, Zoltan', 'wosStandard': 'Süle, Z', 'researcherId': 'AAF-9797-2021'}, {'displayName': 'Abonyi, Janos', 'wosStandard': 'Abonyi, J', 'researcherId': 'O-2832-2013'}]"


def cleanup_authors(authors):
    formatted_authors = "; ".join([author["displayName"] for author in authors])
    return formatted_authors


if __name__ == "__main__":
    column_map = {
        "uid": "uid",
        "title": "title",
        "identifiers.doi": "doi",
        "sourceTypes": "type",
        "source.publishYear": "year",
        "source.volume": "volume",
        "source.issue": "issue",
        "names.authors": "authors",
        "identifiers.issn": "issn",
        "keywords.authorKeywords": "keywords",
    }
    load_dotenv()
    api_key = os.getenv("WOS_API_KEY")
    combinations = get_search_combos()
    generate(api_key=api_key, combinations=combinations)
