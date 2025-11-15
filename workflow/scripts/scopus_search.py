import pandas as pd
import itertools
from tqdm import tqdm
import pybliometrics

pybliometrics.init()
from pybliometrics.scopus import ScopusSearch


if __name__ == "__main__":
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
    gov_terms = ["govern*", "regula*", "legal"]
    trust_terms = ["explain*", "interpret*", "trust*", "uncertainty"]
    combinations = list(
        itertools.product(
            population_terms, interv_terms_ai, interv_terms_decision, outcome_terms
        )
    )
    results = []
    searches = []
    for pop, intervention_ai, intervention_dm, outcome in tqdm(combinations):
        query1 = f"TITLE-ABS-KEY ( {pop} ) AND TITLE-ABS-KEY ( {intervention_ai} W/5 {intervention_dm}) AND TITLE-ABS-KEY ( {outcome} ) AND PUBYEAR AFT 2014 AND DOCTYPE(ar)"

        # query2 = f"TITLE-ABS-KEY ( {pop} ) AND TITLE-ABS-KEY ( {intervention_ai} ) AND TITLE-ABS-KEY ( {outcome} ) AND TITLE-ABS-KEY( {trust} ) AND PUBYEAR AFT 2014"

        s = ScopusSearch(query1, download=True)

        # df = pd.DataFrame(s.results)
        n = s.get_results_size()
        searches.append((f"{pop}, {intervention_ai}, {outcome}: {n}\n"))
        if n == 0:
            continue
        else:
            results.append(pd.DataFrame(s.results))
        # print(df.head())

    df = pd.concat(results)
    df.drop_duplicates(inplace=True)
    total_papers = len(df)
    print(f"TOTAL PAPERS: {total_papers}")
    print(f"RESULTS: {df.head()}")
    df.to_csv(snakemake.output.results)
    with open(snakemake.output.metrics, "w") as file:
        file.writelines(searches)
