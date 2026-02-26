import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_countries(df):
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
    plt.savefig('../../paper/figs/countries.png', dpi=300)
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
    plt.savefig('../../paper/figs/ai_type.png', dpi=300)
    return

if __name__=="__main__":
    df = pd.read_csv('../../results/data_extraction.csv', 
                 usecols=['AI Type - Intervention', 'Comparison', 'Country', 'Data Type', 'Date','Decision Making - (Intervention)', 'Deployed?', 'Feature Study?', 'Industry', 'Output Feature','Place', 'Published Year', 'QA Score', 'Regulatory Oversight Body (if any)', 'Safety Outcome', 'Study','Subcategory', 'Was explainability/interpretability considered?'])
    plot_countries(df)
    plot_ai_type(df)