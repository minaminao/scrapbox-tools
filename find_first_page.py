import sys
from pathlib import Path
import json
import time

assert len(sys.argv) == 2, f"Usage: python {sys.argv[0]} <json>"

filename = sys.argv[1]
filepath = Path(filename)
pages = json.load(filepath.open())["pages"]


min_created = None
first_page_title = None
for page in pages:
    created = page["created"]
    if min_created == None or created < min_created:
        min_created = created
        first_page_title = page["title"]

print(first_page_title, time.localtime(min_created))
    

