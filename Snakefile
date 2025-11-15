rule targets:
    input:
        scopus_results = 'results/scopus_searches.csv',
        wos_results = 'results/wos_searches.csv', 

rule search_scopus:
    input:
        parfiles = 'environment.yml',
    output:
        metrics = 'results/scopus_metrics.txt',
        results = 'results/scopus_searches.csv', 
    script:
        'workflow/scripts/scopus_search.py'

rule search_wos:
    input:
        parfiles = 'environment.yml',
    output:
        results = 'results/wos_searches.csv', 
    script:
        'workflow/scripts/wos_search.py'

rule generate_bib_files:
    input:
        search_results = ['results/scopus_searches.csv', 'results/wos_searches.csv'],
    output:
        bib_files = ['results/scopus.bib', 'results/wos.bib'],
    script:
        'workflow/scripts/bib.py'

rule build_dag:
    input: "Snakefile"
    output:
        "dag.png"
    shell:
        "snakemake --dag | dot -Tpng > {output}"