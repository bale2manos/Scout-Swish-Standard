import os
import shutil


def remove_initial_wrong_chars(text):
    chars_mistaken = ['O', '9']
    for char in chars_mistaken:
        if text[0] == char or text[0] == 'o' or text[0] == '0':
            text = text[1:]

        # If first three chars are (0)
        if text[0] == '(' and text[1] == char and text[2] == ')':
            text = text[3:]

        if text[0] == '(' and text[1] == char:
            text = text[2:]
    return text


def simplify_path(path):
    # Define a mapping from special characters to their simpler equivalents
    replacements = {
        'ñ': 'n',
        'Ñ': 'N',
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U'
    }
    for char, replacement in replacements.items():
        path = path.replace(char, replacement)
    return path


def time_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    except ValueError:
        return 0


def create_temp_copy(image_path):
    # Simplify the path by replacing special characters
    simplified_path = simplify_path(image_path)
    # Define the path to copy the file
    base_dir = os.path.dirname(simplified_path)
    base_name = os.path.basename(simplified_path)
    temp_path = os.path.join(base_dir, f"temp_{base_name}")
    # Copy the file to the new path
    shutil.copy(image_path, temp_path)
    return temp_path


def clean_text_and_remove_excess(text):
    lines = text.split('\n')
    lines = [line for line in lines if line]

    print("Lines originally: ", lines)

    if lines[0] == '0':
        return

    print("Lines after removing 0: ", lines)
    # Remove points because they are repeated, remove lines [1]
    if len(lines) > 1:
        # If there are more than 2 numbers after the colon, add the next numbers into a new cell in lines list
        if len(lines) > 2 and len(lines[2]) > 5:
            # Remove the numbers from the second line
            lines[2] = lines[2][:5]
            aux = lines[2]
            lines[2] = lines[1]
            lines[1] = aux
        else:
            lines[3] = lines[1]
            lines.pop(1)


    # Join lines into one string
    text = '\n'.join(lines)
    if '%\n' not in text:
        text = text.replace('%', '%\n')
    lines = text.split('\n')
    lines = [line for line in lines if line]

    return lines
