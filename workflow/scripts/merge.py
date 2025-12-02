import numpy as np
import pandas as pd


if __name__ == "__main__":
    scopus_file = "../../results/scopus_searches.csv"
    wos_file = "../../results/wos_searches.csv"
    output_file = "../../results/all.csv"
    # load both csvs into pandas dataframes
    # scopus_df = pd.read_csv(snakemake.input.scopus_csv)
    # wos_df = pd.read_csv(snakemake.input.wos_scv)

    scopus_df = pd.read_csv(scopus_file, index_col=0)
    wos_df = pd.read_csv(wos_file, index_col=0)
    # merge the dataframes
    df = pd.concat([wos_df, scopus_df])
    if len(df) != len(scopus_df) + len(wos_df):
        raise ValueError("Merged dataframe lost or gained too many rows!")
    # drop duplicates using doi
    cleaned_df = df.drop_duplicates(subset=["doi"])
    print(len(cleaned_df), len(df))
    # rewrite to csv
    cleaned_df.to_csv(output_file)
    # save


# import bibtexparser

# def load_scopus(bibfile):
#     return bib_string

# def load_wos(bibfile):
#     return bib_string

# def check_duplicates(scopus, wos):
#     return cleaned_string

# if __name__=="__main__":
#     # load scopus bibliography as a string

#     # load wos bibliography as a string

#     # merge and delete duplicate entries

#     # convert the cleaned string to a bibfile again

#     # save the bibfile
