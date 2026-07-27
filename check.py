import requests,json,os
from bs4 import BeautifulSoup
URL="https://mittlopp.se/Marknad/NXQEPQUCWFDLPVAJVP?lang=sv#sell"
TOPIC=os.environ["NTFY_TOPIC"]
STATE="seen.json"
seen=set(json.load(open(STATE))) if os.path.exists(STATE) else set()
html=requests.get(URL,timeout=20).text
soup=BeautifulSoup(html,"html.parser")
text=soup.get_text(" ",strip=True)
if "Just nu finns det inga startplatser till försäljning" in text:
    print("No listings"); raise SystemExit
links=[]
for a in soup.find_all("a",href=True):
    h=a["href"]
    if "Marknad" in h or "sell" in h: links.append(h)
new=[l for l in set(links) if l not in seen] or ["listing"]
for item in new:
    requests.post(f"https://ntfy.sh/{TOPIC}",data=f"Ny startplats! {URL}".encode())
seen.update(new)
json.dump(sorted(seen),open(STATE,"w"))
