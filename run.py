import re
import requests
import bibtexparser
from unidecode import unidecode

def generate_readable_key(entry):
    if "author" not in entry or "year" not in entry or "title" not in entry:
        return None
    first_author = entry["author"].split("and")[0].strip().split()[-1]
    year = entry.get("year", "xxxx")[:4]
    title_word = re.sub(r"[^\w\s]", "", entry["title"].lower().strip()).split()
    short_title = ''.join(title_word[:2])
    return unidecode(f"{first_author}{year}{short_title}")

def query_dblp_by_title(title):
    query = '+'.join(title.lower().strip().split())
    url = f"https://dblp.org/search/publ/api?q={query}&format=json"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"})
    if response.status_code != 200:
        return None
    data = response.json()
    hits = data.get("result", {}).get("hits", {}).get("hit", [])
    return hits

def fetch_bibtex_from_dblp_url(url):
    if not url.endswith(".html"):
        return None
    bibtex_url = url.replace(".html", ".bib")
    r = requests.get(bibtex_url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36"})
    return r.text if r.status_code == 200 else None

def is_arxiv_entry(entry):
    return ("arxiv" in entry.get("doi", "").lower() or
            "arxiv" in entry.get("pages", "").lower() or
            "arxiv" in entry.get("url", "").lower())

def process_and_replace(entry):
    if not is_arxiv_entry(entry):
        return entry, None

    title = entry.get("title", "")
    dblp_hits = query_dblp_by_title(title)
    if not dblp_hits:
        return entry, None

    for hit in dblp_hits:
        dblp_url = hit.get("info", {}).get("url", "") + '.html'
        bibtex_text = fetch_bibtex_from_dblp_url(dblp_url)
        if bibtex_text:
            parser = bibtexparser.loads(bibtex_text)
            if parser.entries:
                return parser.entries[0], bibtex_text
    return entry, None

def process_bib_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    new_entries = []
    replaced = 0
    for entry in bib_database.entries:
        updated_entry, new_bib = process_and_replace(entry)
        updated_entry["ID"] = generate_readable_key(updated_entry) or entry["ID"]
        if new_bib:
            print(f"✔ Replaced arXiv: {entry['ID']} ➜ {updated_entry['ID']}")
            replaced += 1
        new_entries.append(updated_entry)

    new_bib = bibtexparser.bibdatabase.BibDatabase()
    new_bib.entries = new_entries

    with open(output_path, "w", encoding="utf-8") as bibtex_file:
        bibtexparser.dump(new_bib, bibtex_file)

    print(f"\n🔄 Total replaced: {replaced}")

# 用法：
if __name__ == "__main__":
    import argparse
    args = argparse.ArgumentParser(description="Process and replace arXiv entries in a BibTeX file.")
    args.add_argument("input_file", type=str, help="Input BibTeX file path")
    args.add_argument("output_file", type=str, help="Output BibTeX file path")
    args = args.parse_args()
    process_bib_file(args.input_file, args.output_file)