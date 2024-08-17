from PIL import Image
import pytesseract
import os

tesseract_cmd_path = r'F:/Programas/Tesseract-OCR/tesseract.exe'


def crop_image_to_top(image_path, output_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Get the dimensions of the image
        width, height = img.size

        # Get two thirds width
        two_thirds_width = 3 * width // 4

        # Calculate the dimensions of the top-left quarter
        new_height = height // 15

        # Start with a height offset of 5% of the original height
        new_height_offset = 3*(height // 40)
        bottom_point = new_height + (height // 21)


        # Define the box to crop (left, upper, right, lower)
        box = (0, new_height_offset, two_thirds_width, bottom_point )

        # Crop the image
        cropped_img = img.crop(box)

        # Save the cropped image
        cropped_img.save(output_path)

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

    # Remove the characters that are numbers inside the string
    if text[0] == 'O' or text[0] == 'o' or text[0] == '0':
        text = text[1:]

    # If first three chars are (0)
    if text[0] == '(' and text[1] == 'O' and text[2] == ')':
        text = text[3:]

    if text[0] == '(' and text[1] == 'O':
        text = text[2:]

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


def crop_image_to_second_third_row(image_path, output_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Get the dimensions of the image
        width, height = img.size

        # Get two thirds width
        left_crop = 18 * (width // 19)

        # Calculate the height of each section
        sections = height // 3

        # Topside offset
        topside_offset = sections // 10
        bottomside_offset = sections // 9

        top_point = sections + 2 * topside_offset
        bottom_point = 2 * sections - bottomside_offset

        # Define the box to crop (left, upper, right, lower)
        # The cropping box starts at the top of the second third and ends at the bottom of the image
        box = (0, top_point, left_crop, bottom_point)

        # Crop the image
        cropped_img = img.crop(box)

        # Save the cropped image in the output path
        cropped_img.save(output_path)

    print(f"Cropped image saved to {output_path}")

def crop_image_to_second_fifth_row(image_path, output_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Get the dimensions of the image
        width, height = img.size

        # Calculate the height of each section
        sections = height // 5
        width_max = 9 * width // 10

        # Topside offset
        topside_offset = 2 * sections
        bottomside_offset = 2.2 * sections

        box = (0, topside_offset, width_max, bottomside_offset)

        # Crop the image
        cropped_img = img.crop(box)

        # Save the cropped image in the output path
        cropped_img.save(output_path)

        # Remove the image file
        #os.remove(image_path)

    print(f"Cropped image saved to {output_path}")