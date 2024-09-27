# Scrape teanglann.ie

This project is designed to scrape and process data from the FGB (Foclóir Gaeilge-Béarla) related to verbal nouns and other verb forms in the Irish language.

## Project Structure

- `scrape_fgb_vns/words.txt`: Contains a list of words to be processed.
- `scrape_fgb_vns/process_json_data.py`: Script to process JSON data and extract specific verb forms.
- `scrape_fgb_vns/process_json_data_r_root.py`: Process JSON data and extract specific verb forms using the Present root.

## Requirements

- Python 3.x
- `output.json` file containing the data to be processed.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/scrape_teanglann.git
    cd scrape_teanglann
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages (if any):
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Ensure you have the `output.json` file in the root directory of the project.

2. Run the processing scripts:
    ```sh
    python scrape_fgb_vns/process_json_data.py
    python scrape_fgb_vns/process_json_data_r_root.py
    ```

3. Move output to archive:
    ```sh
    `datetime=$(date '+%Y%m%d_%H%M%S'); for file in output.*; do mv "$file" "./archive/${file%.*}_$datetime.${file##*.}"; done`
    ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.