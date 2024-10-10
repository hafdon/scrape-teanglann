# Function to extract text from specific divs
import requests
from bs4 import BeautifulSoup

from config.logging import setup_logging

logger = setup_logging()


def scrape_definitions(url):
    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    main_div = soup.find("div", class_="dir obverse exacts")
    if not main_div:
        logger.error(f"Main div not found in {url}.")
        return None

    entries = main_div.find_all("div", class_="fgb entry")
    definitions = [entry.get_text(separator=" ", strip=True) for entry in entries]
    full_definition = "\n\n".join(definitions)
    return full_definition
