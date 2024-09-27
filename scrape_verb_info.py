import requests
from bs4 import BeautifulSoup
import csv
import re
import json

def extract_verb_info(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Dictionary to hold the extracted verb information
        verb_info = {}

        # Extract Verbal Noun
        verbal_noun_section = soup.find('h3', string='VERBAL NOUN')
        if verbal_noun_section:
            verbal_noun = verbal_noun_section.find_next('span', class_='value primary').text.strip()
            verb_info['verbal_noun'] = verbal_noun

        # Extract Verbal Adjective
        verbal_adjective_section = soup.find('h3', string='VERBAL ADJECTIVE')
        if verbal_adjective_section:
            verbal_adjective = verbal_adjective_section.find_next('span', class_='value primary').text.strip()
            verb_info['verbal_adjective'] = verbal_adjective

        # Extract tenses
        tense_bodies = soup.find_all('div', class_='body')
        for body in tense_bodies:
            tense_id = body.get('id')
            if not tense_id:
                continue  # Skip if no id
            tense_name = tense_id  # Tense IDs correspond to tense names

            verb_info[tense_name] = {}  # Initialize tense dictionary

            subsections = body.find_all('div', class_='subsection')
            for subsection in subsections:
                form_heading_tag = subsection.find('h3')
                if form_heading_tag:
                    form_heading = form_heading_tag.text.strip().upper()
                else:
                    form_heading = 'UNKNOWN'

                conjugations = extract_conjugation(subsection)
                verb_info[tense_name][form_heading] = conjugations

        return verb_info
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Helper function to extract conjugations from each subsection
def extract_conjugation(subsection):
    conjugations = []
    blocks = subsection.find_all('div', class_='block')

    for block in blocks:
        # For each block, get the primary value and the bulletted values
        lines = block.find_all('div', class_='line')
        for line in lines:
            value_span = line.find('span', class_='value primary')
            if value_span:
                # Primary value
                value = value_span.text.strip()
                # Check if there is a label (e.g., (MASC.), (FEM.))
                label_span = line.find('span', class_='label')
                if label_span:
                    label = label_span.text.strip()
                    value = f"{value} {label}"
                conjugations.append(value)
            else:
                # Bulletted line
                value_span = line.find('span', class_='value')
                if value_span:
                    value = value_span.text.strip()
                    conjugations.append(value)

    return conjugations

# Function to construct URLs
def construct_urls(base_url, words):
    return [f"{base_url}/{word}" for word in words]

# Example base URL and list of words
base_url = "https://www.teanglann.ie/en/gram"
words = []
with open('words.txt', 'r') as file:
    for line in file:
        words.append(line.strip())

# Construct the URLs
urls = construct_urls(base_url, words)

# Extract verb info from all URLs
extracted = {url: extract_verb_info(url) for url in urls}
items_dict = []

# Organize the results into a list of dictionaries for writing to CSV or JSON
for url, item in extracted.items():
    if item:
        match = re.search(r'/([^/]+)$', url)
        if match:
            last_word = match.group(1)
            items_dict.append({'url': last_word, 'item': item})
        else:
            items_dict.append({'url': url, 'item': item})

# Specify the output file paths
output_csv = 'output.csv'
output_json = 'output.json'

# Write the data to a JSON file for better structure
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(items_dict, f, ensure_ascii=False, indent=4)

print(f"Data has been written to {output_json}.")

# Optional: Write a simplified version to CSV if needed
# Flatten the data for CSV output (this will be less detailed)
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    # Define the fieldnames based on the data you want to include
    fieldnames = ['url', 'verbal_noun', 'verbal_adjective']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for entry in items_dict:
        data = {
            'url': entry['url'],
            'verbal_noun': entry['item'].get('verbal_noun', ''),
            'verbal_adjective': entry['item'].get('verbal_adjective', '')
        }
        writer.writerow(data)

print(f"Data has been written to {output_csv}.")
