import requests
from bs4 import BeautifulSoup
import json
import csv
from openai import OpenAI
import logging


client = OpenAI()


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
                        {"word":"doicheallach","adjective_definitions":"(1) churlish, inhospitable","verb_definitions":"(1) to be unwilling to receive someone; (2) to be churlish with someone; (3) to be grudging with something, unwilling to do something","noun_definitions":"(1) churlish, cold welcome; (2) grudging word, smile","other":"(phrase) he gave it grudgingly; (phrase) he is stand-offish in company."}
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
        # overview = structured_data.get("overview_definition", "")
        adjectives = structured_data.get("adjective_definitions", "")
        verbs = structured_data.get("verb_definitions", "")
        nouns = structured_data.get("noun_definitions", "")
        other = structured_data.get("other", "")

        logging.debug(f"structured_data: {structured_data}")
        return (adjectives, verbs, nouns, other)

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

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

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

    try:
        # Iterate over each word and its corresponding URL
        for word, url in zip(words, urls):
            try:
                logging.info(f"Processing word: {word}")
                definition = extract_definitions(url)
                if not definition:
                    logging.warning(
                        f"Skipping word '{word}' due to extraction failure."
                    )
                    continue

                # Ensure get_overview_definition returns a tuple
                overview = get_overview_definition(definition)
                if not overview:
                    logging.warning(
                        f"Skipping word '{word}' because get_overview_definition returned None."
                    )
                    continue

                # Attempt to unpack the overview
                try:
                    adjectives, verbs, nouns, other = overview
                except TypeError as te:
                    logging.error(f"Error unpacking overview for word '{word}': {te}")
                    continue

                # Append to final data
                final_data.append(
                    {
                        "word": word,
                        "adjectives": adjectives,
                        "verbs": verbs,
                        "nouns": nouns,
                        "other": other,
                    }
                )
                logging.info(f"Added definitions for word '{word}'")
            except Exception as e:
                logging.error(f"An error occurred while processing word '{word}': {e}")
                continue  # Continue with the next word

    except KeyboardInterrupt:
        logging.info("Process interrupted by user. Saving data collected so far.")
    except Exception as e:
        logging.error(f"An unexpected error occurred during processing: {e}")
    finally:
        if final_data:
            # Export to CSV
            csv_filename = "words_overview_definitions.csv"

            try:
                with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
                    fieldnames = [
                        "word",
                        "adjectives",
                        "verbs",
                        "nouns",
                        "other",
                    ]

                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for entry in final_data:
                        writer.writerow(entry)

                logging.info(f"Data successfully exported to {csv_filename}")
            except Exception as e:
                logging.error(
                    f"An error occurred while writing to '{csv_filename}': {e}"
                )
        else:
            logging.warning("No data to export.")


if __name__ == "__main__":
    main()
