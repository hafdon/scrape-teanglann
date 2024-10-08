import requests
from bs4 import BeautifulSoup


# Function to extract text from a specific div and save it to a file
def extract_text_to_file(url, filename):
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the div with class "dir obverse exacts"
        target_div = soup.find("div", class_="dir obverse exacts")

        # Check if the div is found
        if target_div:
            # Extract the plain text from the div
            plaintext = target_div.get_text(separator=" ", strip=True)

            # Save the text to a file
            with open(filename, "w", encoding="utf-8") as file:
                file.write(plaintext)

            print(f"Text extracted and saved to {filename}")
        else:
            print("The target div was not found on the page.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


# Define the URL and the output file
url = "https://www.teanglann.ie/en/fgb/d%c3%adon"
filename = "extracted_text.txt"

# Call the function to extract text and save it
extract_text_to_file(url, filename)
