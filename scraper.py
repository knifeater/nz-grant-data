import requests
from bs4 import BeautifulSoup
import json
import datetime

URL = "https://www.business.govt.nz/funding-grants/"
OUTPUT_FILE = "data.json"

def scrape_grants():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    grants = []

    # Look for each grant in the card listing
    cards = soup.find_all("div", class_="card")

    for card in cards:
        try:
            title = card.find("h2").get_text(strip=True)
            description = card.find("p").get_text(strip=True)
            link = card.find("a")["href"]

            # Visit the individual grant page to extract date info
            if link.startswith("/"):
                link = "https://www.business.govt.nz" + link

            grant_page = requests.get(link)
            sub_soup = BeautifulSoup(grant_page.text, "html.parser")

            # This is a best guess; adjust for different grant sites
            open_date = "2025-01-01"
            close_date = "2025-12-31"

            date_tags = sub_soup.find_all("p")
            for tag in date_tags:
                text = tag.get_text().lower()
                if "open" in text:
                    open_date = extract_date(text)
                if "close" in text:
                    close_date = extract_date(text)

            grants.append({
                "name": title,
                "purpose": description,
                "open_date": open_date,
                "close_date": close_date
            })

        except Exception as e:
            print(f"Error scraping card: {e}")
            continue

    # Save to data.json
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grants, f, indent=4)

    print(f"✅ Saved {len(grants)} grants to {OUTPUT_FILE}")

def extract_date(text):
    # Basic fallback parser for "1 June 2025" etc.
    for fmt in ("%d %B %Y", "%d %b %Y"):
        try:
            parts = text.split()
            for i in range(len(parts) - 2):
                date_str = " ".join(parts[i:i+3])
                return datetime.datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except:
            continue
    return "2025-01-01"

if __name__ == "__main__":
    scrape_grants()
