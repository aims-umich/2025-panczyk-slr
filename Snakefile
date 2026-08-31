# ENGINES = ['scopus', 'wos']
ENGINES = ['scopus']
RUN = "original"

rule targets:
    input:
        scopus_results = f'results/{RUN}/scopus_searches.csv',
        wos_results = f'results/{RUN}/wos_searches.csv', 
        prisma = f'results/{RUN}/prisma.txt',
        bib_file = f'results/{RUN}/all_searches.bib',
        small_tree = expand(f'results/{RUN}/small_tree_{{engine}}.png', engine=ENGINES),
        large_tree = expand(f'results/{RUN}/large_tree_{{engine}}.png', engine=ENGINES),
        bar_plot = expand(f'results/{RUN}/bar_{{engine}}.png', engine=ENGINES),

rule generate_search_combinations:
    input:
        parfiles = 'environment.yml',
    output:
        combos = f'results/{RUN}/combos.pkl',
    script:
        'workflow/scripts/combos.py'

rule search_scopus:
    input:
        combos = f'results/{RUN}/combos.pkl',
    output:
        metrics = f'results/{RUN}/scopus_metrics.txt',
        results = f'results/{RUN}/scopus_searches.csv', 
    script:
        'workflow/scripts/scopus_search.py'

rule search_wos:
    input:
        combos = f'results/{RUN}/combos.pkl',
    output:
        metrics = f'results/{RUN}/wos_metrics.txt',
        results = f'results/{RUN}/wos_searches.csv', 
    script:
        'workflow/scripts/wos_search.py'

rule visualize_searches:
    input:
        metrics =  [f'results/{RUN}/scopus_metrics.txt', f'results/{RUN}/wos_metrics.txt'],
        # metrics =  ['results/scopus_metrics.txt'],
    output:
        small_tree = expand(f'results/{RUN}/small_tree_{{engine}}.png', engine=ENGINES),
        large_tree = expand(f'results/{RUN}/large_tree_{{engine}}.png', engine=ENGINES),
        bar_plot = expand(f'results/{RUN}/bar_{{engine}}.png', engine=ENGINES),
    script:
        'workflow/scripts/viz.py'


rule merge_searches:
    input:
        scopus_csv = f'results/{RUN}/scopus_searches.csv',
        wos_csv = f'results/{RUN}/wos_searches.csv',
    output:
        merged_csv = f'results/{RUN}/all_searches.csv',
        prisma = f'results/{RUN}/prisma.txt',
    script:
        'workflow/scripts/merge.py'

rule generate_bib_files:
    input:
        search_results = f'results/{RUN}/all_searches.csv',
    output:
        bib_file = f'results/{RUN}/all_searches.bib',
    script:
        'workflow/scripts/bib.py'

rule build_dag:
    input: "Snakefile"
    output:
        "dag.png"
    shell:
        "snakemake --dag | dot -Tpng > {output}"