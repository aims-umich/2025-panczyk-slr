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
        "health*",
        "medic*",
        "clinical",
        '"autonomous driving"',
        "transportation",
        "construction",
        "cars",
        "engineering",
        "energy",
        '"sensitive industry"',
    ]
    interv_terms_ai = [
        '"artificial intelligence"',
        '"machine learning"',
        '"neural networks"',
        '"language models"',
    ]
    interv_terms_decision = ["decision*"]
    outcome_terms = [
        "incidents",
        "accidents",
        '"near misses"',
        "injuries",
        "failures",
        '"adverse event"',
    ]
    combinations = list(
        itertools.product(
            population_terms, interv_terms_ai, interv_terms_decision, outcome_terms
        )
    )
    return combinations


def generate(api_key, combinations, output_file):
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
        print(params["q"])
        try:
            data = response.json()["hits"]
        except KeyError:
            print(response.json())
            continue

        if len(data) > 1:
            df = pd.json_normalize(data)
            frames.append(df)
            continue
    result = pd.concat(frames, ignore_index=True, sort=False)
    result["names.authors"] = result["names.authors"].apply(cleanup_authors)
    result["keywords.authorKeywords"] = result["keywords.authorKeywords"].apply(
        cleanup_keywords
    )
    result["sourceTypes"] = result["sourceTypes"].apply(cleanup_sourcetype)

    useful_columns = list(column_map.keys())
    result = result[useful_columns]
    result.rename(columns=column_map, inplace=True)
    result.to_csv(output_file)


def cleanup_authors(authors):
    formatted_authors = "; ".join([author["displayName"] for author in authors])
    return formatted_authors


def cleanup_keywords(keywords):
    # the bar thing is dumb but do it to match scopus
    formatted_keywords = "| ".join([k for k in keywords])
    return formatted_keywords


def cleanup_sourcetype(source):
    formatted_keywords = ",".join([s for s in source])
    return formatted_keywords


if __name__ == "__main__":
    column_map = {
        "uid": "uid",
        "title": "title",
        "identifiers.doi": "doi",
        "sourceTypes": "subtypeDescription",
        "source.publishYear": "year",
        "source.volume": "volume",
        "source.issue": "issue",
        "names.authors": "author_names",
        "identifiers.issn": "issn",
        "keywords.authorKeywords": "authkeywords",
    }
    load_dotenv()
    api_key = os.getenv("WOS_API_KEY")
    combinations = get_search_combos()
    generate(
        api_key=api_key, combinations=combinations, output_file=snakemake.output.results
    )
