import pandas as pd
import itertools
from tqdm import tqdm
import pybliometrics
import pickle

pybliometrics.init()
from pybliometrics.scopus import ScopusSearch


if __name__ == "__main__":
    with open(snakemake.input.combos, "rb") as f:
        combinations = pickle.load(f)
    results = []
    searches = []
    conf_query = "CONFNAME('NEURIPS*' OR 'ICLR*' OR 'ICML*' OR 'AAAI*' OR 'IJCAI*')"
    for pop, intervention_ai, intervention_dm, outcome in tqdm(combinations):
        query1 = f"TITLE-ABS-KEY ( {pop} ) AND TITLE-ABS-KEY ( {intervention_ai} W/5 {intervention_dm}) AND TITLE-ABS-KEY ( {outcome} ) AND PUBYEAR AFT 2014 AND PUBYEAR BEF 2026 AND (DOCTYPE(ar) OR (DOCTYPE(cp) AND {conf_query}))"

        try:
            s = ScopusSearch(query1, download=True)
        except:
            print(f"Failed on: {query1}")

        # df = pd.DataFrame(s.results)
        n = s.get_results_size()
        searches.append((f"{pop}, {intervention_ai}, {outcome}, {n}\n"))
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
