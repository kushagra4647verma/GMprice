import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.investorgain.com/report/live-ipo-gmp/331/all/"

response = requests.get(URL, headers={
    "User-Agent": "Mozilla/5.0"
})
soup = BeautifulSoup(response.text, "lxml")

rows = soup.select("#report_table tbody tr")
ipos = []

for row in rows:
    if row.get("class") == ["tbody-repeated-header"] or row.find("th"):
        continue

    cells = row.find_all("td")
    if len(cells) < 10:
        continue

    name = cells[0].get_text(strip=True)
    gmp = cells[1].get_text(strip=True)
    rating = cells[2].get_text(strip=True)
    subscription = cells[3].get_text(strip=True)
    gmp_range = cells[4].get_text(strip=True)
    price = cells[5].get_text(strip=True)
    ipo_size = cells[6].get_text(strip=True)
    lot = cells[7].get_text(strip=True)
    open_date = cells[8].get_text(strip=True)
    close_date = cells[9].get_text(strip=True)
    boa_date = cells[10].get_text(strip=True)
    listing = cells[11].get_text(strip=True)
    updated_on = cells[12].get_text(strip=True)

    if len(name) < 3:
        continue

    ipos.append({
        "name": name,
        "gmp": gmp,
        "rating": rating,
        "subscription": subscription,
        "gmpRange": gmp_range,
        "price": price,
        "ipoSize": ipo_size,
        "lot": lot,
        "open": open_date,
        "close": close_date,
        "boaDate": boa_date,
        "listing": listing,
        "updatedOn": updated_on
    })

with open("data/ipo.json", "w") as f:
    json.dump({
        "updated": True,
        "timestamp": response.headers.get("date"),
        "count": len(ipos),
        "ipos": ipos
    }, f, indent=2)

print("IPO data updated successfully.")
