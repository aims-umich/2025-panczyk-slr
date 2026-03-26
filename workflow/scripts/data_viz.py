import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd

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
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16


# def plot_countries(df):
#     fig, ax = plt.subplots(figsize=(12,8))
#     country_series = (
#         df['Country']
#         .dropna()
#         .str.split(',')
#         .explode()
#         .str.strip()
#     )
#     sns.countplot(y=country_series, order=country_series.value_counts().index, color="lavender", ax=ax)
#     ax.set_xlabel('Number of Articles with at Least One Contribution from Country Listed')
#     plt.tight_layout()
#     plt.savefig('../../paper/figs/countries.pgf')
#     return 

def plot_countries(df, version='map'):
    # MUST TURN OFF PGF PLOTTING PARAMS FOR THIS TO WORK
    if version=='map':
        geo_df = gpd.read_file('World_Countries_Generalized_Shapefile/World_Countries_Generalized.shp')[['COUNTRY', 'geometry']]
        geo_df.columns = ['Country', 'geometry']
        geo_df = geo_df.drop(geo_df.loc[geo_df['Country'] == 'Antarctica'].index)
        
        df = df[df['Country'] != 'International Collaboration']
        country_counts = (
        df['Country']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
        .value_counts()
        .reset_index()
        )
        country_counts.columns = ['Country', 'Count']
        merged = pd.merge(geo_df, country_counts)
        vmin = merged['Count'].min()
        vmax = merged['Count'].max()
        cmap = 'Purples'
        fig, ax = plt.subplots(figsize=(14,8))
        ax.axis('off')
        # ax.set_title('Article Density by Country', fontdict={'fontsize': '20', 'fontweight': '3'})
        geo_df.plot(ax=ax, edgecolor='black', facecolor='white', linewidth=0.1)
        merged.plot(column='Count', edgecolor='black', linewidth=0.1, cmap=cmap, ax=ax)
        sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax), cmap=cmap)
        # Empty array for the data range
        sm._A = []
        # Add the colorbar to the figure
        cbaxes = fig.add_axes([0.15, 0.25, 0.01, 0.4])
        cbar = fig.colorbar(sm, cax=cbaxes)
        plt.savefig('../../paper/figs/countries_map.pdf', dpi=300)
    else:
        fig, ax = plt.subplots(figsize=(12,8))
        country_series = (
            df['Country']
            .dropna()
            .str.split(',')
            .explode()
            .str.strip()
        )
        sns.countplot(y=country_series, order=country_series.value_counts().index, color="lavender", ax=ax)
        ax.set_xlabel('Number of Articles with at Least One Contribution from Country Listed')
        plt.tight_layout()
        plt.savefig('../../paper/figs/countries.pdf')
    return 

def plot_ai_type(df):
    fig, ax = plt.subplots(figsize=(12,8))
    df = df[df['AI Type - Intervention'] != 'Non Applicable']
    ai_series = (
        df['AI Type - Intervention']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
    )
    sns.countplot(y=ai_series, order=ai_series.value_counts().index, color="lightsteelblue", ax=ax)
    ax.set_xlabel('Number of Articles Employing AI Type')
    plt.tight_layout()
    plt.savefig('../../paper/figs/ai_type.pgf')
    return

def plot_explainability(df):
    fig, ax = plt.subplots(figsize=(12,8))
    df = df[df['XAI Type'] != 'Non-Applicable']
    ai_series = (
        df['XAI Type']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
    )
    sns.countplot(y=ai_series, order=ai_series.value_counts().index, color="lightgreen", ax=ax)
    ax.set_xlabel('Explainability Type and Frequency, If Considered')
    plt.tight_layout()
    plt.savefig('../../paper/figs/explain_type.pgf')
    return

def plot_DM_type(df):
    fig, ax = plt.subplots(figsize=(12,8))
    df = df[df['Decision Making - (Intervention)'] != 'Non Applicable']
    ai_series = (
        df['Decision Making - (Intervention)']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
    )
    sns.countplot(y=ai_series, order=ai_series.value_counts().index, color="lightcoral", ax=ax)
    ax.set_xlabel('Decision-Making Type Frequency')
    plt.tight_layout()
    plt.savefig('../../paper/figs/dm_type.pgf')
    return

def plot_QA(df):
    fig, ax = plt.subplots()
    sns.histplot(df, x='QA Score', color="peachpuff", ax=ax)
    ax.set_xlabel('Quality Score')
    ax.set_ylabel('Article Count')
    plt.tight_layout()
    plt.savefig('../../paper/figs/qa_scores.pgf')
    return

def get_stats(df):
    print(df['Was explainability/interpretability considered?'].unique())
    xai_counts = df['Was explainability/interpretability considered?'].value_counts()
    xai_considered = xai_counts.get('Yes', 0)
    xai_not_considered = xai_counts.get('No', 0)

    print(df['Was regulation considered?'].unique())
    reg_counts = df['Was regulation considered?'].value_counts()
    reg_considered = reg_counts.get('Yes', 0)
    reg_not_considered = reg_counts.get('No', 0)

    print(df['Deployed?'].unique())
    dep_counts = df['Deployed?'].value_counts()
    dep = dep_counts.get('Yes', 0)
    nodep = dep_counts.get('No', 0)
    depna = dep_counts.get('Non Applicable', 0)

    print(f'Deployed: {dep}, Not Deployed: {nodep}, NA: {depna}')

    print(df['Industry'].unique())
    total_papers = df['Industry'].value_counts()
    medical = total_papers.get('Medical', 0)
    manufac = total_papers.get('Manufacturing', 0)
    ethics = total_papers.get('Ethics', 0)
    aviation = total_papers.get('Aviation', 0)
    avs = total_papers.get('Autonomous Vehicles', 0)
    nuclear = total_papers.get('Nuclear', 0)

    print(f'XAI Considered: {xai_considered}, Total: {xai_considered + xai_not_considered}, Ratio: {xai_considered/(xai_considered + xai_not_considered)}')
    print(f'Reg Considered: {reg_considered}, Total: {reg_considered + reg_not_considered}, Ratio: {reg_considered/(reg_considered + reg_not_considered)}')

    print(f'Medical: {medical}, {medical/72}, Manufacturing: {manufac/72}, Ethics: {ethics/72}, Aviation: {aviation/72}, AVs: {avs/72}, Nuclear: {nuclear/72}')
    return


if __name__=="__main__":
    df = pd.read_csv('../../results/data_extraction.csv',
                 usecols=['AI Type - Intervention', 'Comparison', 'Country', 'Data Type', 'Date','Decision Making - (Intervention)', 'Deployed?', 'Feature Study?', 'Industry', 'Output Feature','Place', 'Published Year', 'QA Score', 'Regulatory Oversight Body (if any)', 'Safety Outcome', 'Study','Subcategory', 'Was explainability/interpretability considered?', 'XAI Type', 'Was regulation considered?']
                )

    plot_countries(df)
    # plot_ai_type(df)
    # plot_explainability(df)
    # plot_DM_type(df)
    # plot_QA(df)
    # get_stats(df)