import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import squarify

sns.set_theme(style="whitegrid")


def vizualize(txtfile, save_as="barplot.png"):
    df = pd.read_csv(
        txtfile,
        header=None,
        names=["population", "intervention", "outcome", "count"],
        skipinitialspace=True,
    )

    pop_df = (
        df.groupby(by=["population"])
        .sum()
        .reset_index()
        .drop(columns=["intervention", "outcome"])
        .sort_values(by=["count"], ascending=False)
    )

    intervention_df = (
        df.groupby(by=["intervention"])
        .sum()
        .reset_index()
        .drop(columns=["population", "outcome"])
        .sort_values(by=["count"], ascending=False)
    )

    outcome_df = (
        df.groupby(by=["outcome"])
        .sum()
        .reset_index()
        .drop(columns=["intervention", "population"])
        .sort_values(by=["count"], ascending=False)
    )

    print(type(pop_df))
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    sns.set_color_codes("pastel")
    sns.barplot(x="count", y="population", data=pop_df, label="Population", color="b")
    sns.barplot(
        x="count",
        y="intervention",
        data=intervention_df,
        label="Intervention",
        color="pink",
    )
    sns.barplot(x="count", y="outcome", data=outcome_df, label="Outcome", color="green")
    ax.set_ylabel("Search Term")
    ax.set_xlabel("Count")
    fig.tight_layout()
    fig.savefig(save_as, dpi=300)
    return


def treeplot(txtfile, large=True, save_as="tree.png"):
    df = pd.read_csv(
        txtfile,
        header=None,
        names=["population", "intervention", "outcome", "count"],
        skipinitialspace=True,
    )
    df = df[df["count"] > 0].copy().sort_values(by=["count"], ascending=False)
    # only consider searches with outcomes greater than 10
    if large:
        plot_df = df[df["count"] > 10].copy()
    else:
        plot_df = df[df["count"] <= 10].copy()

    possible_outcomes = plot_df["outcome"].unique()
    print(possible_outcomes)
    color_map = {outcome: plt.cm.Set3(i) for i, outcome in enumerate(possible_outcomes)}
    colors = [color_map[outcome] for outcome in plot_df["outcome"]]

    # Create labels
    labels = [
        f"{row['population']}\n{row['intervention']}\n{row['outcome']}\n({row['count']})"
        for _, row in plot_df.iterrows()
    ]

    plt.figure(figsize=(14, 10))
    plt.axis("off")
    if large:
        squarify.plot(
            sizes=plot_df["count"],
            label=labels,
            alpha=0.8,
            color=colors,
            text_kwargs={"fontsize": 8, "weight": "bold"},
            pad=False,
            ec="gray",
        )
        plt.title(f"Search Results by Term Combinations with > 10 Papers", fontsize=16)
        plt.tight_layout()
        plt.savefig(save_as, dpi=300, bbox_inches="tight")
    else:
        squarify.plot(
            sizes=plot_df["count"],
            label=labels,
            alpha=0.8,
            color=colors,
            text_kwargs={"fontsize": 6, "weight": "bold"},
            pad=False,
        )
        plt.title(
            f"Search Results by Term Combinations with (0,10] Papers", fontsize=16
        )
        plt.tight_layout()
        plt.savefig(save_as, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    # loop over input and output files for first scopus, then web of science
    for metrics_file, small_tree, large_tree, bar_plot in zip(
        snakemake.input.metrics,
        snakemake.output.small_tree,
        snakemake.output.large_tree,
        snakemake.output.bar_plot,
    ):
        vizualize(metrics_file, save_as=bar_plot)
        treeplot(metrics_file, large=True, save_as=large_tree)
        treeplot(metrics_file, large=False, save_as=small_tree)
