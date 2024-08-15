# Image Text Extraction and Data Processing Project

## Overview

This project extracts numerical data from images of sports statistics. It uses OpenCV to preprocess images, Tesseract OCR to extract text, and pandas to save and process the data.

## Requirements

Make sure you have the following Python packages installed:

- `opencv-python`
- `pytesseract`
- `Pillow`
- `pandas`
- `openpyxl`

You can install them using pip:

```bash
pip install opencv-python pytesseract Pillow pandas openpyxl
```

## Setup

1. **Ensure Tesseract is Installed:**
   Tesseract OCR must be installed on your system. You can download it from [Tesseract&#39;s GitHub repository](https://github.com/tesseract-ocr/tesseract) and follow the installation instructions for your operating system.
2. **Update Tesseract Path:**
   If Tesseract is not in your system's PATH, update the `pytesseract.pytesseract.tesseract_cmd` variable in your script to point to the Tesseract executable.

## Running the Project

1. **Prepare Your Images:**
   Place your images in a folder named `Pintobasket`. The images should be named in the format `PlayerName_image.png`.
2. **Run the Script:**
   Execute the Python script by running:

   ```
   python3 scout.py
   ```
3. **Output:**

   The script processes the images, extracts the data, and saves it to an Excel file named `player_data.xlsx` in the same directory.

## Script Details

### Functions

* **`preprocess_image(image_path)`** : Loads and preprocesses the image by drawing rectangles, inverting colors, and resizing.
* **`extract_text(image)`** : Extracts text from the image using Tesseract OCR.
* **`extract_data_from_text(text, player_name)`** : Cleans and processes the extracted text into a structured format.
* **`clean_text_and_remove_excess(text)`** : Cleans up text data to remove excess or incorrect entries.
* **`check_minutes(lines)`, `check_over_5_PF(lines)`, etc.** : Performs specific checks and formatting on the extracted data.
* **`extract_player_name(filename)`** : Extracts the player's name from the image filename.
* **`save_to_excel(data, excel_filename)`** : Saves the processed data to an Excel file and performs additional sorting and tagging.

### Example Usage

Assuming your script is named `scout.py` and your images are in the `Pintobasket` folder, run:

`python3 scout.py`

After execution, the processed data will be saved in `player_data.xlsx`.

## Notes

* Ensure that the file paths and names in the script match your actual setup.
* Adjust the script as needed to fit your specific requirements or data format.
