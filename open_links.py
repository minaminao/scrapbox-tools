import webbrowser
import urllib.parse

links = open("result.txt").readlines()

N = 10
print(f"{len(links)} lines found.")

for i in range(N):
    if links[i].startswith("http"):
        v = links[i].strip().split("//", 1)
        v[-1] = urllib.parse.quote(v[-1])
        url = "//".join(v)
        print(links[i])
        webbrowser.open(url)

with open("result.txt", "w") as f:
    f.writelines(links[N:])