import requests
from bs4 import BeautifulSoup


# Function to extract text from specific divs and save it to a file with line breaks between entries
def extract_text_to_file(url, filename):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the main div with class "dir obverse exacts"
        main_div = soup.find("div", class_="dir obverse exacts")

        # Check if the main div is found
        if main_div:
            # Find all the child divs with class "fgb entry"
            entries = main_div.find_all("div", class_="fgb entry")

            # Prepare a list to hold the text for each entry
            extracted_texts = []

            # Loop through each entry div and extract the text
            for entry in entries:
                entry_text = entry.get_text(separator=" ", strip=True)
                extracted_texts.append(entry_text)

            # Join the text of each entry with a newline between them
            full_text = "\n\n".join(extracted_texts)

            # Save the text to a file
            with open(filename, "w", encoding="utf-8") as file:
                file.write(full_text)

            print(f"Text extracted and saved to {filename}")
        else:
            print("The target div was not found on the page.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


# Define the URL and the output file
url = "https://www.teanglann.ie/en/fgb/d%c3%adon"
filename = "extracted_text_with_line_breaks.txt"

# Call the function to extract text and save it
extract_text_to_file(url, filename)
