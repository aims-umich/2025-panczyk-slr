import csv
from pybtex.database import BibliographyData, Entry, Person
import numpy as np

# THIS SCRIPT WAS CREATED LARGELY BY CLAUDE AND CHECKED BY NATALY


def csv_to_bibtex(csv_file, output_file="output.bib"):
    """Convert CSV to BibTeX using pybtex."""

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"CSV Reader found {len(rows)} rows. Type: {type(rows)}")

    bib_data = BibliographyData()
    cite_keys = []
    counter = 0

    for idx, row in enumerate(rows, 0):
        # Generate citation key
        first_author = row.get("author_names", "").split(";")[0].strip()
        last_name = first_author.split(",")[0].strip()
        if not row.get("year"):
            year = row.get("coverDate", "")[:4]
        else:
            year = row.get("year").strip()
        # string formatting here to eliminate any whitespace
        cite_key_candidate = f"{last_name}{year}".replace(" ", "")
        if cite_key_candidate in cite_keys:
            cite_key = f"{last_name}{year}_{idx}"
            cite_keys.append(cite_key)
        else:
            cite_key = cite_key_candidate
            cite_keys.append(cite_key)

        # Parse authors
        authors = []
        if row.get("author_names"):
            for author in row["author_names"].split(";"):
                author = author.strip()
                if author:
                    authors.append(Person(author))

        # Build entry fields
        fields = {}

        if row.get("title"):
            fields["title"] = row["title"].strip()
        if row.get("publicationName"):
            fields["journal"] = row["publicationName"].strip()
        if year:
            fields["year"] = year
        if row.get("volume"):
            fields["volume"] = row["volume"].strip()
        if row.get("issueIdentifier"):
            fields["number"] = row["issueIdentifier"].strip()
        if row.get("pageRange"):
            fields["pages"] = row["pageRange"].strip()
        if row.get("doi"):
            fields["doi"] = row["doi"].strip()
        if row.get("issn"):
            fields["issn"] = row["issn"].strip()
        if row.get("description"):
            fields["abstract"] = row["description"].strip()
        if row.get("authkeywords"):
            fields["keywords"] = row["authkeywords"].strip().replace("|", ",").lower()
        if row.get("pubmed_id"):
            fields["pmid"] = row["pubmed_id"].strip()
        if row.get("publisher"):
            fields["publisher"] = row["publisher"].strip()

        # Create entry (use 'article' for journal articles)
        entry = Entry("article", fields=fields, persons={"author": authors})
        bib_data.entries[cite_key] = entry
        counter += 1

    # Write to file
    bib_data.to_file(output_file, bib_format="bibtex")
    print(f"BibTeX file created: {output_file}")
    print(f"Total entries: {len(bib_data.entries)}")
    print(counter)


# Usage
if __name__ == "__main__":
    # for csv_f, outfile in zip(
    #     snakemake.input.search_results, snakemake.output.bib_files
    # ):
    #     csv_to_bibtex(csv_f, outfile)
    csv_to_bibtex("../../results/all.csv", "../../results/all.bib")
