import requests
import os
from dotenv import load_dotenv
import itertools
from tqdm import tqdm
import pandas as pd
import json
import pickle


def generate(api_key, combinations, output_file, metrics_file):
    headers = {"X-ApiKey": api_key}
    url = "https://api.clarivate.com/apis/wos-starter/v1/documents"
    frames = []
    conf_query = "SO=(NEURIPS* OR ICLR* OR ICML* OR AAAI* OR IJCAI*)"
    for pop, interv_ai, interv_dm, outcome in tqdm(combinations):
        page = 1
        n_matches = 51
        while page * 50 <= n_matches:
            params = {
                "db": "WOS",
                "q": f"TS=({pop}) AND TS=({interv_ai} NEAR/5 {interv_dm}) AND TS=({outcome}) AND PY=2015-2026 AND (DT=Article OR (DT=Proceedings Paper AND ({conf_query})))",
                "limit": 50,
                "page": page,
            }
            response = requests.get(url, headers=headers, params=params)
            response_json = response.json()
            page += 1
            try:
                n_matches = response_json["metadata"]["total"]
                data = response_json["hits"]
            except KeyError:
                print("KEY ERROR")
                print(response.json())
                n_matches = 0
                continue
            if len(data) > 0:
                df = pd.json_normalize(data)
                frames.append(df)
        with open(metrics_file, "a") as f:
            f.write(f"{pop}, {interv_ai}, {outcome}: {n_matches} \n")

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
    with open(snakemake.input.combos, "rb") as f:
        combinations = pickle.load(f)
    generate(
        api_key=api_key,
        combinations=combinations,
        output_file=snakemake.output.results,
        metrics_file=snakemake.output.metrics,
    )
