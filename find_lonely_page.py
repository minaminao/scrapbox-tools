import json
import re
import sys
from pathlib import Path

assert len(sys.argv) == 2, f"Usage: python {sys.argv[0]} <json>"

filename = sys.argv[1]
filepath = Path(filename)
pages = json.load(filepath.open())["pages"]

# 現状外部リンクも含んでいる
pattern = re.compile(r"(\[[^\*/\$\-!][^\]]*\]|#[^\s]+)")

normalized_title_to_title = {}


def normalize_title(title: str):
    global normalize_title_to_title
    normalized_title = title.lower().replace("_", " ")
    normalized_title_to_title[normalized_title] = title
    return normalized_title


def calc_deg(page_titles=None):
    in_deg = {}
    out_deg = {}
    for page in pages:
        normalized_title = normalize_title(page["title"])
        lines = page["lines"]
        for line in lines:
            matches = re.findall(pattern, line)
            for link in matches:
                if link[0] == "#":
                    link = link[1:]
                else:
                    link = link[1:-1]
                link = normalize_title(link)
                if page_titles is not None and link not in page_titles:
                    continue
                in_deg[link] = in_deg.get(link, 0) + 1
                out_deg[normalized_title] = out_deg.get(normalized_title, 0) + 1
    return in_deg, out_deg


in_deg, out_deg = calc_deg()
page_titles = set([normalize_title(page["title"]) for page in pages])
for normalized_title, deg in in_deg.items():
    if deg >= 2:
        page_titles.add(normalized_title)
in_deg, out_deg = calc_deg(page_titles)

lonely_page_titles = []
for page in pages:
    normalized_title = normalize_title(page["title"])
    if normalized_title not in in_deg and normalized_title not in out_deg:
        lonely_page_titles.append(normalized_title_to_title[normalized_title])

for title in lonely_page_titles:
    project_name = sys.argv[1].replace(".json", "")
    print(f"https://scrapbox.io/{project_name}/{title.replace(' ', '_')}")

print(f"Found {len(lonely_page_titles)} lonely pages.")
