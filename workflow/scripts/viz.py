import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import squarify
import matplotlib as mpl

mpl.use("pgf")
plt.rcParams['pgf.texsystem'] = 'pdflatex'
plt.rcParams['text.usetex'] = True
plt.rcParams['pgf.rcfonts'] = False
plt.rcParams['figure.edgecolor'] = 'k'
plt.rcParams['figure.facecolor'] = 'w'
plt.rcParams['savefig.dpi'] = 600
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['font.family'] = "serif"
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16

# sns.set_theme(style="whitegrid")


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
    fig, ax = plt.subplots(1, 1, figsize=(10, 13))
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
    ax.tick_params(axis='both', labelsize=18)
    ax.legend(
    prop={'size': 18},          # Bigger legend text
    title_fontsize=14,
    markerscale=1.5,            # Bigger legend color patches
    )
    fig.tight_layout()
    plt.savefig(save_as, bbox_inches='tight')
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
        plot_df = df[df["count"] > 4].copy()
    else:
        plot_df = df[df["count"] <= 4].copy()

    possible_outcomes = plot_df["outcome"].unique()
    print(possible_outcomes)
    color_map = {outcome: plt.cm.Set3(i) for i, outcome in enumerate(possible_outcomes)}
    colors = [color_map[outcome] for outcome in plot_df["outcome"]]

    # Create labels
    labels = [
        f"{row['population']}\n{row['intervention']}\n{row['outcome']}\n({row['count']})"
        for _, row in plot_df.iterrows()
    ]

    plt.figure(figsize=(16, 12))
    plt.axis("off")
    if large:
        squarify.plot(
            sizes=plot_df["count"],
            label=labels,
            alpha=0.8,
            color=colors,
            text_kwargs={"fontsize": 14, "weight": "bold"},
            pad=False,
            ec="gray",
        )
        # plt.title(f"Search Results by Term Combinations with Greater Than Four Papers", fontsize=16)
        plt.tight_layout()
        plt.savefig(save_as, bbox_inches="tight")
    else:
        squarify.plot(
            sizes=plot_df["count"],
            label=labels,
            alpha=0.8,
            color=colors,
            text_kwargs={"fontsize": 6, "weight": "bold"},
            pad=False,
        )
        plt.title(f"Search Results by Term Combinations with (0,4] Papers", fontsize=16)
        plt.tight_layout()
        plt.savefig(save_as, bbox_inches="tight")


if __name__ == "__main__":
    ## FOR SNAKEMAKE, UNCOMMENT BELOW:
    # loop over input and output files for first scopus, then web of science
    # for metrics_file, small_tree, large_tree, bar_plot in zip(
    #     snakemake.input.metrics,
    #     snakemake.output.small_tree,
    #     snakemake.output.large_tree,
    #     snakemake.output.bar_plot,
    # ):
    #     vizualize(metrics_file, save_as=bar_plot)
    #     treeplot(metrics_file, large=True, save_as=large_tree)
    #     treeplot(metrics_file, large=False, save_as=small_tree)

    ## FOR MANUAL, UNCOMMENT BELOW:
    metrics_files = ['../../results/scopus_metrics.txt', '../../results/wos_metrics.txt']
    small_trees = ['../../paper/figs/small_tree_scopus.pgf', '../../paper/figs/small_tree_wos.pgf']
    large_trees = ['../../paper/figs/large_tree_scopus.pgf', '../../paper/figs/large_tree_wos.pgf']
    bar_plots = ['../../paper/figs/bar_scopus.pgf', '../../paper/figs/bar_wos.pgf']

    for metrics_file, small_tree, large_tree, bar_plot in zip(
        metrics_files,
        small_trees,
        large_trees,
        bar_plots,
    ):
        vizualize(metrics_file, save_as=bar_plot)
        treeplot(metrics_file, large=True, save_as=large_tree)
        treeplot(metrics_file, large=False, save_as=small_tree)
