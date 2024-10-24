"""
This script extracts grammatical information (specifically, the genitive plural form) for a list of Irish words from the Teanglann.ie website and writes the results to a CSV file.

It reads a list of words from 'words.txt', constructs URLs to access their grammatical information, extracts the genitive plural form, and saves the results in 'output.csv'.
"""

import requests
import csv
from bs4 import BeautifulSoup
import re
import argparse


def scrape_genitive_value(scrape_url):
    """
    Extracts the genitive singular form of a noun from the given URL.

    Parameters:
        scrape_url (str): The URL of the word's grammatical page on Teanglann.ie.

    Returns:
        str or None: The genitive singular form of the noun if found, otherwise None.
    """
    try:
        # Fetch the HTML content from the URL
        response = requests.get(scrape_url)
        # Ensure that the request was successful
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all 'gram' sections (grammatical information)
        noun_sections = soup.find_all("div", class_="gram")
        genitive_value = None

        for section in noun_sections:
            # Find if this section contains the header 'NOUN'
            header_value = section.find("div", class_="header").find(
                "div", class_="value"
            )
            if header_value and header_value.text.strip() == "NOUN":
                # Find the Singular section
                singular_section = section.find("div", class_="section")

                if singular_section:
                    # Find all subsections in the singular section
                    subsections = singular_section.find_all("div", class_="subsection")

                    for subsection in subsections:
                        # Look for the h3 tag that contains the text 'GENITIVE'
                        if subsection.find("h3", string="GENITIVE"):
                            # Extract the genitive singular form
                            genitive_value_span = subsection.find(
                                "span", class_="value primary"
                            )
                            if genitive_value_span:
                                genitive_value = genitive_value_span.text.strip()
                                break  # Exit the loop once the genitive value is found

        return genitive_value

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page. Error: {e}")
        return None


def scrape_declension(url):
    """
    Extracts the declension of a noun from the given URL.

    Parameters:
        url (str): The URL of the word's grammatical page on Teanglann.ie.

    Returns:
        str: The declension information if found, or an error message.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the elements containing declension information
        declensions = (
            soup.find("div", class_="dir obverse exacts")
            .find("div", class_="gram")
            .find_all("div", class_="property")
        )

        # Extract the declension text
        for prop in declensions:
            if "DECLENSION" in prop.text:
                return prop.text.strip()
    else:
        return f"Failed to retrieve content. Status code: {response.status_code}"


def extract(extraction_urls, fn):
    """
    Applies a given extraction function to a list of URLs and collects the results.

    Parameters:
        extraction_urls (list of str): The list of URLs to extract data from.
        fn (function): The extraction function to apply to each URL.

    Returns:
        dict: A dictionary mapping each URL to the result of the extraction function.
    """
    # Dictionary to store URL and its corresponding extracted value
    results = {}

    for word_url in extraction_urls:
        word_elem = fn(word_url)
        # Add the result to the dictionary
        results[word_url] = word_elem
        print(f"Processed {word_url}: {word_elem}")

    return results


def extract_adjective_class(url):
    """
    Extracts the class number of an adjective from the given URL.

    Parameters:
        url (str): The URL of the adjective's page on Teanglann.ie.

    Returns:
        str or None: The class number of the adjective if found, otherwise None.
    """
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the div with class 'fgb entry'
        entry_div = soup.find("div", class_="fgb entry")
        if not entry_div:
            print("Error: 'fgb entry' div not found.")
            return None

        # Within the entry_div, find the span with class 'fgb g'
        fgb_g_span = entry_div.find("span", class_="fgb g")
        if not fgb_g_span:
            print("Error: 'fgb g' span not found.")
            return None

        # Remove the nested span with class 'fgb tip' to isolate the number
        tip_span = fgb_g_span.find("span", class_="fgb tip")
        if tip_span:
            tip_span.extract()  # Remove it from the parse tree

        # Get the remaining text and extract the number using regex
        text_content = fgb_g_span.get_text(strip=True)
        value_match = re.search(r"\d+", text_content)
        if value_match:
            return value_match.group()
        else:
            print("Error: Numeric value not found.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None


def extract_definitions(url):
    """
    Extracts the definitions of a word from the given URL.

    Parameters:
        url (str): The URL of the word's entry on Teanglann.ie.

    Returns:
        str or None: A formatted string of definitions if found, otherwise None.
    """
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the div with class 'fgb entry'
        entry_div = soup.find("div", class_="fgb entry")
        if not entry_div:
            print("Error: 'fgb entry' div not found.")
            return None

        # Find all spans with class 'fgb trans' within the entry_div
        trans_spans = entry_div.find_all("span", class_="fgb trans")
        if not trans_spans:
            print("Error: 'fgb trans' spans not found.")
            return None

        # Extract and format the definitions
        definitions = []
        for i, trans_span in enumerate(trans_spans, 1):
            # Extract the definition text
            definition_text = trans_span.get_text(separator=" ", strip=True)
            definitions.append(f"{i}. {definition_text}")

        # Join the extracted definitions into a single string
        result = " ".join(definitions)
        return result

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None


def extract_plural_genitive(url):
    """
    Extracts the genitive plural form of a noun from the given URL.

    Parameters:
        url (str): The URL of the word's grammatical page on Teanglann.ie.

    Returns:
        str or None: The genitive plural form if found, otherwise None.
    """
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all sections with class 'section'
        sections = soup.find_all("div", class_="section")
        if not sections:
            print("Error: No sections found.")
            return None

        # Iterate over all sections to find the 'Plural' section
        for section in sections:
            # Check if this section has an <h2> with the text 'Plural'
            header = section.find("h2")
            if header and header.get_text(strip=True) == "Plural":
                # Within the 'Plural' section, find all subsections
                subsections = section.find_all("div", class_="subsection")
                if not subsections:
                    print("Error: No subsections found in 'Plural' section.")
                    return None

                # Iterate over all subsections to find the 'GENITIVE' subsection
                for subsection in subsections:
                    subheader = subsection.find("h3")
                    if subheader and subheader.get_text(strip=True) == "GENITIVE":
                        # Find the primary value inside the 'GENITIVE' subsection
                        primary_value_span = subsection.find(
                            "span", class_="value primary"
                        )
                        if primary_value_span:
                            # Extract and return the text from the primary value span
                            return primary_value_span.get_text(strip=True)
                        else:
                            print(
                                "Error: 'value primary' span not found in 'GENITIVE' subsection."
                            )
                            return None

        print("Error: 'Plural' 'GENITIVE' section not found.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None


def construct_urls(word_base_url, word_list):
    """
    Constructs full URLs by appending words to a base URL.

    Parameters:
        word_base_url (str): The base URL.
        word_list (list of str): The list of words to append to the base URL.

    Returns:
        list of str: The list of constructed URLs.
    """
    return [f"{word_base_url}/{word}" for word in word_list]


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Extract genitive plural forms of Irish words from Teanglann.ie and save to CSV."
    )
    parser.add_argument(
        "-i",
        "--input",
        default="words.txt",
        help="Path to the input text file containing Irish words (default: words.txt)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.csv",
        help="Path to the output CSV file (default: output.csv)",
    )
    args = parser.parse_args()

    base_url = "https://www.teanglann.ie/en/gram"

    # Read words from the input file
    words = []
    with open(args.input, "r", encoding="utf-8") as file:
        for line in file:
            words.append(line.strip())

    # Construct the URLs
    urls = construct_urls(base_url, words)

    # Extract the genitive plural forms for all URLs
    extracted = extract(urls, extract_plural_genitive)

    # Prepare the data for CSV writing
    items_list = []

    # Process the extracted results
    for url, item in extracted.items():
        print(f"URL: {url} -> Genitive Plural Form: {item}")
        # Extract the word from the URL
        match = re.search(r"/([^/]+)$", url)
        if match:
            word = match.group(1)
            items_list.append({"word": word, "genitive_plural": item})
        else:
            # If unable to extract the word, use the full URL
            items_list.append({"word": url, "genitive_plural": item})

    # Write the data to the output CSV file
    with open(args.output, mode="w", newline="", encoding="utf-8") as file:
        # Create a CSV writer object and specify the fieldnames
        writer = csv.DictWriter(file, fieldnames=["word", "genitive_plural"])

        # Write the header (column names)
        writer.writeheader()

        # Write each dictionary entry as a row
        writer.writerows(items_list)

    print(f"Data has been written to {args.output}.")


if __name__ == "__main__":
    main()
