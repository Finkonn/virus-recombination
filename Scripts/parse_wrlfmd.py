import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "https://www.wrlfmd.org/fmdv-genome/fmd-prototype-strains"

response = requests.get(URL, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

tabs = {}

for a in soup.select("a.nav-link[role='tab']"):
    serotype_raw = a.get_text(strip=True)
    serotype = serotype_raw.replace(" ", "")
    panel_id = a.get("href", "").lstrip("#")

    if panel_id:
        tabs[serotype] = panel_id
rows = []

for serotype, panel_id in tabs.items():
    panel = soup.find(id=panel_id)
    if panel is None:
        continue

    current_topotype = None

    for el in panel.find_all(["h3", "table"], recursive=True):

        if el.name == "h3":
            current_topotype = el.get_text(strip=True)

        elif el.name == "table":
            headers = [th.get_text(strip=True) for th in el.find_all("th")]

            for tr in el.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all("td")]
                if not cells:
                    continue

                row = {
                    "Serotype": serotype,
                    "Topotype": current_topotype,
                }

                for h, v in zip(headers, cells):
                    row[h] = v

                rows.append(row)

df = pd.DataFrame(rows)
df.to_excel("wrlfmd_prototype_strains.xlsx", index=False)
