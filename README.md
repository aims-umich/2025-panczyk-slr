# 2025-panczyk-slr

This repository serves to reproduce the results found in [When computers call the shots --- exploring the impact of AI in high-stakes decision-making]().

## Paper Citation
Paper citation will go here!

## Abstract
While applications abound for the modern surge of artificial-intelligence (AI)-based technologies, we owe special care to those in which *human lives are at stake*. Perilously, AI advances faster than the regulations that protect us from it. As such, in this review, **we explore the impact of AI on high-stakes decision-making.** Though reviews have attempted adjacent analyses before, none have effectively targeted safety-critical industries or considered the relation between AI developers, users, and regulators.

To address these gaps, we conduct a systematic literature review. We cast a wide net in our search, then filter with a series of criteria that qualify a system's sensitivity, decision-making framework, and risk. After distilling our initial pool of 1,135 papers into a final subset of 72 reports, we identify critical features of AI systems and industry implementation practices that demonstrate: 1) the safety risks of using AI in high-stakes decision-making, 2) how we can mitigate these risks, and 3) how we can assign responsibility for AI-based decisions.
A major finding of our review is that, contrary to popular broad calls for increasing model interpretability and explainability, we find these features only useful in specific safety-critical scenarios-- when the user has both the *expertise and time* to review a model output. Such cases do not require regulation to authorize user trust, and we expect overregulation to be counterproductive. Alternatively, when expertise or time is limited, validation (*not* explanation) techniques and robust regulation *must* authorize user trust. This review bridges the gap among developers, users, and regulators regarding safety-critical AI applications and offers specific recommendations for policy and future work based on its findings.

## Data Extraction Results
Data extraction results are available in: `results/data_extraction.csv`.

## Bibliographies
The initial retrieved article bibliography is available in: `results/all_searches.bib` or `results/all_searches.csv`.

The final full paper bibliography (including non-retrieved sources) is available in: `paper/bibliography.bib`.

## Getting Started
### Requirements
- python

All necessary packages included in `environment.yml`

### Environment Setup and Activation

```bash
conda env create -f environment.yml

conda activate lit-review
```

### API Setup
Running this script requires both a Scopus API and a Web of Science API. If you only want to query from a single database, the `Snakefile` can be modified to only include one database in the workflow. 

#### Scopus
This workflow uses `pybliometrics` to query Scopus. The first time you run the `scopus_search` rule, it will trigger `pybliometics.init()`. This will prompt you to enter your Scopus API key in the terminal, but you will only have to do this the first time. You can acquire an API at the [Elsevier Developer Portal](https://dev.elsevier.com/apikey/manage).

#### Web of Science
To access the Web of Science database, this workflow uses the Web of Science Starter API v1. You can apply for this API at the [Web of Science Developer Portal](https://developer.clarivate.com/apis/wos-starter). To activate this API, you will need to create a `.env` file in the main directory fo this repo and include the following line: 

```python
WOS_API_KEY=yourapikeyhere
```

If you have access to a different Web of Science API, you may adapt the `url` variable in the `generate()` function in `workflow/scripts/wos_search.py` to accommodate your alternate API url. 

## How to Generate Results

All results reproducible via 

```bash
snakemake -j1
```

Indivdual rules can be run by repeating the command above but inserting the rule name found in the `Snakefile`. For example, to just re-run the scopus search

```bash
snakemake search_scopus -j1
```

## License

[MIT](https://choosealicense.com/licenses/mit/)