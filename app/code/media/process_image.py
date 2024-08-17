import os

from ..data.excel import save_to_excel
from ..data.text_to_data import extract_player_name, extract_data_from_text
from ..media.image_to_text import extract_text
from ..media.preprocess_image import preprocess_image_adding_rectangles, preprocess_image


def process_images(folder_path, excel_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and filename != 'GENERAL_STATS.png':
            image_path = os.path.join(folder_path, filename)
            try:
                print(f"Processing {image_path}...")
                preprocessed_image = preprocess_image_adding_rectangles(image_path)
                text = extract_text(preprocessed_image)
                player_name = extract_player_name(filename)
                player_data = extract_data_from_text(text, player_name)
                if player_data:
                    data.append(player_data)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    save_to_excel(data, excel_path)


def get_team_stats(image_path):
    scaled_image = preprocess_image(image_path)

    text = extract_text(scaled_image)

    lines = text.split('\n')
    lines = [line for line in lines if line]
    sections = ['Wins', 'Loses', 'Avg Points Scored', 'Avg Points Received']
    data = {}
    for i in range(len(lines)):
        if i < len(sections):
            data[sections[i]] = lines[i]

    # Check not over 150 points scored or received
    if ('Avg Points Scored' in data) and float(data['Avg Points Scored']) > 150:
            data['Avg Points Scored'] = data['Avg Points Scored'][:2] + '.' + data['Avg Points Scored'][2:]

    if ('Avg Points Received' in data) and float(data['Avg Points Received']) > 150:
        data['Avg Points Received'] = data['Avg Points Received'][:2] + '.' + data['Avg Points Received'][2:]

    print(data)
    return data
