import requests
from bs4 import BeautifulSoup
import json
import csv
from openai import OpenAI

client = OpenAI()

import logging

# Configure logging
logging.basicConfig(
    filename="program.log",  # Log file name
    filemode="a",  # Append mode
    level=logging.DEBUG,  # Minimum log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
)

# Also, set up logging to console if needed
console = logging.StreamHandler()
console.setLevel(logging.INFO)  # Adjust as needed
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


# Function to extract text from specific divs
def extract_definitions(url):
    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    main_div = soup.find("div", class_="dir obverse exacts")
    if not main_div:
        logging.error(f"Main div not found in {url}.")
        return None

    entries = main_div.find_all("div", class_="fgb entry")
    definitions = [entry.get_text(separator=" ", strip=True) for entry in entries]
    full_definition = "\n\n".join(definitions)
    return full_definition


# Function to get Overview Definition from OpenAI
def get_overview_definition(definition):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                        You are an Irish language learning assistant, helping users improve their understanding, vocabulary, pronunciation, and grammar in the Irish language.

                        When provided with a detailed word entry containing definitions in a structured list (e.g., numbered or bullet points), extract and list the key definitions in a simplified single-line, paragraph-style format. Each definition should include the part of speech followed by a concise definition, separated by a semicolon.
                        
                        Please return this as structured data.
                        
                        example:
                        { "word": "díon", "overview_definition": "(noun) a form of protection or shelter from elements and harm; (verb) to protect or cover something."}
                        """,
                },
                {
                    "role": "user",
                    "content": definition,
                },
            ],
            temperature=0.3,
            max_tokens=500,
        )
        content = completion.choices[0].message.content.strip()
        logging.debug(f"Raw OpenAI response: {completion.choices[0].message.content}")

        # Parse the JSON response
        structured_data = json.loads(content)
        overview = structured_data.get("overview_definition", "")
        logging.debug(f"Received overview_definition: {overview}")
        return overview

    except json.JSONDecodeError as jde:
        logging.error(f"JSON decoding failed: {jde}")
        logging.debug(f"Received content: {content}")
        return None
    except Exception as e:
        logging.error(f"Error with OpenAI API: {e}")
        return None


def main():
    base_url = "https://www.teanglann.ie/en/fgb"
    urls = []
    words = []

    try:
        # Read words and construct URLs
        with open("words.txt", "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()
                if word:
                    words.append(word)
                    urls.append(f"{base_url}/{word}")
        logging.info(f"Loaded {len(words)} words from words.txt")
    except FileNotFoundError:
        logging.critical("The file 'words.txt' was not found.")
        return
    except Exception as e:
        logging.critical(f"An error occurred while reading 'words.txt': {e}")
        return

    # List to hold final data
    final_data = []

    # Iterate over each word and its corresponding URL
    for word, url in zip(words, urls):
        logging.info(f"Processing word: {word}")
        definition = extract_definitions(url)
        if not definition:
            logging.warning(f"Skipping word '{word}' due to extraction failure.")
            continue

        overview_definition = get_overview_definition(definition)
        if not overview_definition:
            logging.warning(f"Skipping word '{word}' due to OpenAI API failure.")
            continue

        # Append to final data
        final_data.append({"word": word, "overview_definition": overview_definition})
        logging.info(f"Added overview_definition for word '{word}'")

    if not final_data:
        logging.warning("No data to export.")
        return

    # Export to CSV
    csv_filename = "words_overview_definitions.csv"

    try:
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["word", "overview_definition"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in final_data:
                writer.writerow(entry)

        logging.info(f"Data successfully exported to {csv_filename}")

    except Exception as e:
        logging.error(f"An error occurred while writing to '{csv_filename}': {e}")


if __name__ == "__main__":
    main()
