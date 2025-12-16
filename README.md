# 2025-panczyk-pylit

This repository serves to reproduce the results found in [Safety First-- The Impact of AI on High-Stakes Decision-Making and How We Regulate It]().

## Paper Citation
Paper citation will go here!

## Abstract
Abstract will go here!

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

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)