from _typeshed import SupportsWrite

import requests
import csv
from bs4 import BeautifulSoup
import re

def scrape_genitive_value(scrape_url):
    try:
        # Fetch the HTML content from the URL
        response = requests.get(scrape_url)
        # Ensure that the request was successful
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the 'gram' section containing the NOUN information
        noun_section = soup.find_all('div', class_='gram')
        genitive_value = None

        for section in noun_section:
            # Find if this section contains the header 'NOUN'
            header = section.find('div', class_='header')
            if header is None:
                continue  # Skip this iteration if header is not found

            header_value = header.find('div', class_='value')
            if header_value is None:
                print("header_value is None")
                continue  # Skip this iteration if header value is not found

            # Check if the value is 'NOUN'
            if header_value.text.strip() == 'NOUN':
                print("header_value.text.strip() == NOUN")
                # Find the Singular section
                singular_section = section.find('div', class_='section')
                # print(singular_section)

                # Find the GENITIVE subsection within Singular
                if singular_section is None:
                    continue  # Skip if singular_section is not found

                # Find all subsections in the singular section
                subsections = singular_section.find_all('div', class_='subsection')

                for subsection in subsections:
                    # Look for the h3 tag that contains the text 'GENITIVE'
                    h3_tag = subsection.find('h3', string='GENITIVE')
                    if h3_tag:
                        # Find the line with the primary value (the first 'line' with 'value primary')
                        genitive_line = subsection.find('div', class_='block').find('div', class_='line')

                        if genitive_line:
                            # Extract the text from 'value primary' span
                            genitive_value = genitive_line.find('span', class_='value primary').text.strip()
                            break  # Exit the loop once the genitive value is found

        return genitive_value

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page. Error: {e}")
        return None

def scrape_declension(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element that contains "2nd DECLENSION"
        # This assumes the structure you provided
        declension = soup.find('div', class_='dir obverse exacts').find('div', class_='gram').find_all('div',
                                                                                                       class_='property')

        # Extract the text for "2nd DECLENSION"
        for prop in declension:
            if "DECLENSION" in prop.text:
                return prop.text.strip()
    else:
        return f"Failed to retrieve content. Status code: {response.status_code}"

def extract(extraction_urls, fn):
    # Dictionary to store URL and its corresponding verbal noun value
    results = {}

    for word_url in extraction_urls:
        word_elem = fn(word_url)
        # Add the result to the dictionary
        results[word_url] = word_elem
        print(word_url, word_elem)

    return results

def extract_adjective_class(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the div with class 'fgb entry'
        entry_div = soup.find('div', class_='fgb entry')
        if not entry_div:
            print("Error: 'fgb entry' div not found.")
            return None

        # Within the entry_div, find the span with class 'fgb g'
        fgb_g_span = entry_div.find('span', class_='fgb g')
        if not fgb_g_span:
            print("Error: 'fgb g' span not found.")
            return None

        # Remove the nested span with class 'fgb tip' to isolate the number
        tip_span = fgb_g_span.find('span', class_='fgb tip')
        if tip_span:
            tip_span.extract()  # Remove it from the parse tree

        # Get the remaining text and extract the number using regex
        text_content = fgb_g_span.get_text(strip=True)
        value_match = re.search(r'\d+', text_content)
        if value_match:
            return value_match.group()
        else:
            print("Error: Numeric value not found.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None

def extract_definitions(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the div with class 'fgb entry'
        entry_div = soup.find('div', class_='fgb entry')
        if not entry_div:
            print("Error: 'fgb entry' div not found.")
            return None

        # Find all spans with class 'fgb trans' within the entry_div
        trans_spans = entry_div.find_all('span', class_='fgb trans')
        if not trans_spans:
            print("Error: 'fgb trans' spans not found.")
            return None

        # Extract and format the definitions
        definitions = []
        for i, trans_span in enumerate(trans_spans, 1):
            # Find the nested span containing the definition text
            definition_text = trans_span.get_text(separator=' ', strip=True)
            definitions.append(f"{i}. {definition_text}")

        # Join the extracted definitions into a single string
        result = ' '.join(definitions)
        return result

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None

def extract_plural_nominative(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all sections
        sections = soup.find_all('div', class_='section')
        if not sections:
            print("Error: No sections found.")
            return None

        # Iterate over all sections to find the 'Plural' section
        for section in sections:
            # Check if this section has an <h2> with the text 'Plural'
            header = section.find('h2')
            if header and header.get_text(strip=True) == 'Plural':
                # Within the 'Plural' section, find all subsections
                subsections = section.find_all('div', class_='subsection')
                if not subsections:
                    print("Error: No subsections found in 'Plural' section.")
                    return None

                # Iterate over all subsections to find the 'NOMINATIVE' subsection
                for subsection in subsections:
                    subheader = subsection.find('h3')
                    if subheader and subheader.get_text(strip=True) == 'GENITIVE':
                        # Find the primary value inside the 'NOMINATIVE' subsection
                        primary_value_span = subsection.find('span', class_='value primary')
                        if primary_value_span:
                            # Extract and return the text from the primary value span
                            return primary_value_span.get_text(strip=True)
                        else:
                            print("Error: 'value primary' span not found in 'NOMINATIVE' subsection.")
                            return None

        print("Error: 'Plural' 'NOMINATIVE' section not found.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None

def construct_urls(word_base_url, word_words):
    # Use list comprehension to construct URLs
    word_base_urls = [f"{word_base_url}/{word_word}" for word_word in word_words]
    return word_base_urls

# Example base URL and list of words
base_url = "https://www.teanglann.ie/en/gram"
words = []
with open('words.txt', 'r') as file:
    for line in file:
        words.append(line.strip())

# Construct the URLs
urls = construct_urls(base_url, words)

# Print the constructed URLs
# print(urls)

# Get the verbal nouns for all URLs
extracted = extract(urls, extract_plural_nominative)
items_dict = []

# Print the results
for url, item in extracted.items():
    print(f"URL: {url} -> form: {item}")
    match = re.search(r'/([^/]+)$', url)
    if match:
        last_word = match.group(1)
        items_dict.append({'url': last_word, 'item': item})
    else:
        items_dict.append({'url': url, 'item': item})


# Specify the output CSV file path
output_file = 'output.csv'

# Write dictionary to a CSV file
with open(output_file, mode='w', newline='') as file:  # type: SupportsWrite[str]
    # Create a CSV writer object and specify the fieldnames
    writer = csv.DictWriter(file, fieldnames=["url", "item"])

    # Write the header (column names)
    writer.writeheader()

    # Write each dictionary entry as a row
    writer.writerows(items_dict)

print(f"Data has been written to {output_file}.")