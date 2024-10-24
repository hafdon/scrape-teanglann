
### What the Script Does

1. **Reads Words from a File**: It reads a list of Irish words from `words.txt`, where each word is on a separate line.

2. **Constructs URLs**: For each word, it constructs a URL that points to its grammatical information on the Teanglann.ie website.

3. **Scrapes Data**: It uses the `extract` function along with `extract_plural_genitive` to scrape the genitive plural form of each noun from the website.

4. **Processes Results**: It collects the results into a list of dictionaries, each containing the word and its genitive plural form.

5. **Writes to CSV**: It writes the collected data to an output CSV file named `output.csv`.

### Function Breakdown

- **`scrape_genitive_value`**: Extracts the genitive singular form of a noun.
- **`scrape_declension`**: Retrieves the declension information of a noun.
- **`extract`**: General-purpose function to apply a specific extraction function to a list of URLs.
- **`extract_adjective_class`**: Extracts the class number of an adjective.
- **`extract_definitions`**: Retrieves definitions of a word.
- **`extract_plural_genitive`**: Extracts the genitive plural form of a noun.
- **`construct_urls`**: Constructs full URLs by appending words to a base URL.
- **`main`**: Orchestrates the execution of the script.

### How to Use the Script

1. **Prepare `words.txt`**: Create a text file named `words.txt` and list all the Irish words you want to process, one word per line.

2. **Run the Script**: Execute the script in a Python environment. Ensure you have the required libraries installed (`requests`, `beautifulsoup4`, etc.).

3. **Check `output.csv`**: After the script completes, check the `output.csv` file for the results.

### Requirements

- **Python 3.x**
- **Libraries**:
  - `requests`
  - `beautifulsoup4`
  - `csv`
  - `re`

### Notes

- The script includes error handling for HTTP requests and missing HTML elements.
- It uses UTF-8 encoding to handle Irish characters with accents.
- The `extract` function is versatile and can be used with different extraction functions for other grammatical data.

Feel free to modify the script or functions based on your specific needs or to extract additional grammatical information.


#### **How to Run the Script with Arguments**

```bash
python irish_genitive_plural_scraper.py -i my_words.txt -o my_output.csv
```

- **`-i` or `--input`**: Specifies the input file containing the list of words.
- **`-o` or `--output`**: Specifies the output CSV file.

If you don't provide these arguments, the script defaults to `words.txt` for input and `output.csv` for output.
