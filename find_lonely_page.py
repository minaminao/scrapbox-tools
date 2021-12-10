import json
import re
import sys
from pathlib import Path

assert len(sys.argv) == 2, f"Usage: python {sys.argv[0]} <json>"

filename = sys.argv[1]
filepath = Path(filename)
pages = json.load(filepath.open())["pages"]

in_deg = {}
out_deg = {}
page_titles = set([page["title"] for page in pages])

# 現状外部リンクも含んでいる
pattern = re.compile(r"(\[[^\*/\$\-!][^\]]+\]|#[^\s]+)")

for page in pages:
    title = page["title"]
    lines = page["lines"]
    for line in lines:
        matches = re.findall(pattern, line)
        for link in matches:
            if link[0] == "#":
                link = link[1:]
            else:
                link = link[1:-1]
            if link not in page_titles:
                continue
            in_deg[link] = in_deg.get(link, 0) + 1
            out_deg[title] = out_deg.get(title, 0) + 1

lonely_page_titles = []
for page in pages:
    title = page["title"]
    if title not in in_deg and title not in out_deg:
        lonely_page_titles.append(title)

for title in lonely_page_titles:
    project_name = sys.argv[1].replace(".json", "")
    print(f"https://scrapbox.io/{project_name}/{title.replace(' ', '_')}")

print(f"Found {len(lonely_page_titles)} lonely pages.")
