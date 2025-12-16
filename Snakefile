ENGINES = ['scopus', 'wos']
# ENGINES = ['scopus']

rule targets:
    input:
        scopus_results = 'results/scopus_searches.csv',
        wos_results = 'results/wos_searches.csv', 
        prisma = 'results/prisma.txt',
        bib_file = 'results/all_searches.bib',
        small_tree = expand('results/small_tree_{engine}.png', engine=ENGINES),
        large_tree = expand('results/large_tree_{engine}.png', engine=ENGINES),
        bar_plot = expand('results/bar_{engine}.png', engine=ENGINES),

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

rule visualize_searches:
    input:
        metrics =  ['results/scopus_metrics.txt', 'results/wos_metrics.txt'],
        # metrics =  ['results/scopus_metrics.txt'],
    output:
        small_tree = expand('results/small_tree_{engine}.png', engine=ENGINES),
        large_tree = expand('results/large_tree_{engine}.png', engine=ENGINES),
        bar_plot = expand('results/bar_{engine}.png', engine=ENGINES),
    script:
        'workflow/scripts/viz.py'


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