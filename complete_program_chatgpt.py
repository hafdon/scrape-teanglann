import requests
from bs4 import BeautifulSoup
import json
import csv
import re
from openai import OpenAI
import mistune

client = OpenAI()

# Set your OpenAI API key
# openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual OpenAI API key


# Function to extract text from specific divs
def extract_definitions(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    main_div = soup.find("div", class_="dir obverse exacts")
    if not main_div:
        print(f"Main div not found in {url}.")
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
            # temperature=0.3,
            # max_tokens=500,
        )
        content = completion.choices[0].message.content

        return content
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None


# Function to parse OpenAI markdown response
def parse_overview_definition(markdown_text):
    markdown_parser = mistune.create_markdown(renderer=None)
    ast = markdown_parser(markdown_text)

    overview = ""
    for element in ast:
        print(element)
        if element["type"] == "heading" and any(
            "Overview Definition" in child.get("raw", "")
            for child in element.get("children", [])
        ):
            # The next element should be the paragraph containing the overview
            next_index = ast.index(element) + 1
            if next_index < len(ast):
                overview_elements = ast[next_index]["children"]
                overview = "".join(
                    [
                        child.get("raw", "")
                        for child in overview_elements
                        if child.get("raw")
                    ]
                )
                break
    return overview.strip()


def main():
    base_url = "https://www.teanglann.ie/en/fgb"
    urls = []
    words = []

    # Read words and construct URLs
    with open("words.txt", "r", encoding="utf-8") as file:
        for line in file:
            word = line.strip()
            if word:
                words.append(word)
                urls.append(f"{base_url}/{word}")

    # List to hold final data
    final_data = []

    # Iterate over each word and its corresponding URL
    for word, url in zip(words, urls):
        print(f"Processing word: {word}")
        definition = extract_definitions(url)
        if not definition:
            print(f"Skipping word '{word}' due to extraction failure.")
            continue

        # Get Overview Definition from OpenAI
        overview_markdown = get_overview_definition(definition)
        if not overview_markdown:
            print(f"Skipping word '{word}' due to OpenAI API failure.")
            continue

        # Parse the Overview Definition

        print("overview_markdown", overview_markdown)
        overview = parse_overview_definition(overview_markdown)

        if not overview:
            print(f"Overview Definition not found for word '{word}'.")
            continue

        # Append to final data
        final_data.append({"word": word, "overview_definition": overview})

    # Export to CSV
    csv_filename = "words_overview_definitions.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["word", "overview_definition"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in final_data:
            writer.writerow(entry)

    print(f"Data successfully exported to {csv_filename}")


if __name__ == "__main__":
    main()
