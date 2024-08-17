from PIL import Image
import pytesseract
import os

from ..media.cropping import crop_image_to_top
from ..utils.utils import remove_initial_wrong_chars

tesseract_cmd_path = r'F:/Programas/Tesseract-OCR/tesseract.exe'


def read_text_from_image(image_path, tesseract_cmd_path):
    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

    # Open the image file
    with Image.open(image_path) as img:
        # Perform OCR on the image
        text = pytesseract.image_to_string(img, lang='spa')
        print(f"Extracted text: {text}")
        # Remove any leading or trailing whitespace
        text = text.strip()

    text = remove_initial_wrong_chars(text)

    # Remove any leading or trailing whitespace
    text = text.strip()

    # Remove last character if it isnt a letter (also remove numbers)
    if not text[-1].isalpha():
        text = text[:-1]

    if text[-1] == '1':
        text[-1] = 'I'

    # Capitalize the first letter of each word
    text = text.title()

    # If the text has as ',' and doesnt have a space after it, add it
    if ',' in text and text[text.index(',')+1] != ' ':
        text = text[:text.index(',')+1] + ' ' + text[text.index(',')+1:]

    # Remove the image file
    os.remove(image_path)

    return text


def get_player_name(image_path,output_path):
    crop_image_to_top(image_path, output_path)
    return read_text_from_image(output_path, tesseract_cmd_path)


def extract_text(image):
    image_pil = Image.fromarray(image)
    custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789.:%-'

    extracted_text = pytesseract.image_to_string(image_pil, config=custom_config)
    return extracted_text
