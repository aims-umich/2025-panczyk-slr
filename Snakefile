rule targets:
    input:
        scopus_results = 'results/scopus_searches.csv',
        wos_results = 'results/wos_searches.csv', 

rule generate_search_combinations:
    input:
        parfiles = 'environment.yml',
    output:
        combos = 'results/combos.pkl',
    script:
        'workflow/scripts/combos.py'

rule search_scopus:
    input:
        combos = 'results/combos.pkl',
    output:
        metrics = 'results/scopus_metrics.txt',
        results = 'results/scopus_searches.csv', 
    script:
        'workflow/scripts/scopus_search.py'

rule search_wos:
    input:
        combos = 'results/combos.pkl',
    output:
        metrics = 'results/wos_metrics.txt',
        results = 'results/wos_searches.csv', 
    script:
        'workflow/scripts/wos_search.py'

rule merge_searches:
    input:
        scopus_csv = 'results/scopus_searches.csv',
        wos_csv = 'results/wos_searches.csv',
    output:
        merged_csv = 'results/all_searches.csv',
        prisma = 'results/prisma.txt',
    script:
        'workflow/scripts/merge.py'

rule generate_bib_files:
    input:
        search_results = 'results/all_searches.csv',
    output:
        bib_file = 'results/all_searches.bib',
    script:
        'workflow/scripts/bib.py'

rule build_dag:
    input: "Snakefile"
    output:
        "dag.png"
    shell:
        "snakemake --dag | dot -Tpng > {output}"