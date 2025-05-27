import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Setup headless Chrome browser
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Navigate to the grants page
driver.get("https://www.perpetualguardian.co.nz/")

time.sleep(3)  # Wait for page to load (can increase if necessary)

# This part assumes the grants are listed on the homepage or in a predictable section.
# You may need to adjust this if the page structure changes.
grants = []

try:
    # Example: look for elements with grant data
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        text = link.text.lower()
        if "grant" in text or "foundation" in text:
            href = link.get_attribute("href")
            if href:
                grants.append({
                    "name": link.text.strip(),
                    "purpose": "See website for details",
                    "open_date": "TBD",
                    "close_date": "TBD"
                })
except Exception as e:
    print("Error while scraping:", e)

# Close the browser
driver.quit()

# Save to data.json
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(grants, f, indent=2)

print(f"Scraped {len(grants)} grants and saved to data.json")
