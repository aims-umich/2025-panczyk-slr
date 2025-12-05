import numpy as np
import pandas as pd


if __name__ == "__main__":
    # scopus_file = "../../results/scopus_searches.csv"
    # wos_file = "../../results/wos_searches.csv"
    # output_file = "../../results/all.csv"

    scopus_file = snakemake.input.scopus_csv
    wos_file = snakemake.input.wos_csv
    output_file = snakemake.output.merged_csv
    # wos_df = pd.read_csv(snakemake.input.wos_scv)

    # load both csvs into pandas dataframes
    scopus_df = pd.read_csv(scopus_file, index_col=0)
    n_scopus = len(scopus_df)
    wos_df = pd.read_csv(wos_file, index_col=0)
    n_wos = len(wos_df)
    # merge the dataframes
    df = pd.concat([wos_df, scopus_df])
    if len(df) != len(scopus_df) + len(wos_df):
        raise ValueError("Merged dataframe lost or gained too many rows!")
    # drop duplicates using doi
    cleaned_df = df.drop_duplicates(subset=["doi"])
    n_postmerge = len(cleaned_df)
    # rewrite to csv
    cleaned_df.to_csv(output_file)
    with open(snakemake.output.prisma, "w") as f:
        f.write(f"Total papers found with Scopus: {n_scopus} \n")
        f.write(f"Total papers found with Web of Science: {n_wos} \n")
        f.write(f"Total papers found after dropping duplicates: {n_postmerge} \n")
        f.write(
            f"Total duplicates dropped: {n_scopus + n_wos} - {n_postmerge} = {n_scopus + n_wos - n_postmerge} \n"
        )
