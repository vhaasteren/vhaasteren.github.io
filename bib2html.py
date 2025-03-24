#!/usr/bin/env python3

import bibtexparser

def clean_author(name: str) -> str:
    """
    Remove curly braces often found in BibTeX fields.
    E.g. '{van~Haasteren}, Rutger' -> 'van~Haasteren, Rutger'.
    """
    name = name.replace('{', '').replace('}', '')
    return name

def format_authors(author_list):
    """
    Format authors into a string that:
     - If <= 3 authors, list them all.
     - If > 3 authors, list the first 3 + ', et al., inc. Rutger...' if needed.
     - Bold 'van Haasteren' if it appears, etc.
    """
    def maybe_bold_rutger(name):
        # Use a relaxed substring check, or do something more robust as needed.
        if 'van Haasteren' in name or 'van~Haasteren' in name:
            return f"<b>{name}</b>"
        return name

    num_auth = len(author_list)
    if num_auth <= 3:
        # Just join them, bold if Rutger is present
        return ", ".join(maybe_bold_rutger(a.strip()) for a in author_list)
    else:
        # We'll show the first 3 authors:
        first_three = [maybe_bold_rutger(a.strip()) for a in author_list[:3]]
        rutger_in_first3 = any("van Haasteren" in x or "van~Haasteren" in x for x in first_three)
        if rutger_in_first3:
            # Example: "Smith, <b>R. vH</b>, Brown, et al."
            return f"{', '.join(first_three)}, <i>et al.</i>"
        else:
            # Example: "Smith, Jones, Brown, et al., inc. <b>R. vH</b>"
            return f"{', '.join(first_three)}, <i>et al.</i>, <b>inc. Rutger van Haasteren</b>"

def bib_to_html(bibfile, output_html="generated_publications.html"):
    with open(bibfile, 'r') as f:
        bib_database = bibtexparser.load(f)

    entries = bib_database.entries

    html_parts = []
    html_parts.append('---')
    html_parts.append('layout: default')
    html_parts.append('title: Publications')
    html_parts.append('---\n')
    html_parts.append('<h1>{{ page.title }}</h1>\n')

    for entry in entries:
        # Basic metadata extraction
        title = entry.get('title', 'No Title').strip().rstrip('.')
        year = entry.get('year', 'Unknown')
        author_field = entry.get('author', 'Unknown')

        # Remove braces from the entire author_field so we don't see them in the split.
        author_field = author_field.replace('{', '').replace('}', '')

        # Now split by ' and '
        authors = [a.strip() for a in author_field.replace('\n',' ').split(' and ') if a]

        # Format the authors
        authors_str = format_authors(authors)

        # Attempt to find arXiv link and/or DOI
        arxiv_num = entry.get('eprint', '')
        doi_link = entry.get('doi', '')

        # Start building the snippet
        snippet = []
        snippet.append(f"<!-- {title} -->")
        snippet.append('<div class="paper" style="margin-bottom: 2em;">')
        snippet.append(f'<span style="font-size: larger; margin-bottom: 0.5em;">{authors_str} ({year})</span>')
        snippet.append(f'<div>"{title}"</div>')

        links = []
        if arxiv_num:
            links.append(f'<a href="https://doi.org/10.48550/arXiv.{arxiv_num}">arXiv Link</a>')
        if doi_link:
            links.append(f'<a href="https://doi.org/{doi_link}">DOI Link</a>')

        if links:
            snippet.append(f'<div>{", ".join(links)}</div>')
        snippet.append('</div>\n')

        html_parts.extend(snippet)

    with open(output_html, 'w') as outf:
        outf.write("\n".join(html_parts))

    print(f"HTML generated and written to {output_html}")

if __name__ == "__main__":
    bib_to_html("publications.bib", "publications.html")
