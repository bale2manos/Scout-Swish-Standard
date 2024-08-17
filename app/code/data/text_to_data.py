import os

from ..utils.utils import clean_text_and_remove_excess
from ..utils.validator import check_data


def extract_data_from_text(text, player_name):
    sections = ['Total Games', 'Avg Minutes', 'Avg Points', 'Avg Free throws', 'Avg 2-points', 'Avg 3-points',
                'Avg Personal fouls', 'Avg +/-',
                'Total Minutes', 'Total Points', 'Total Free throws', 'Free throws percentage', 'Total 2-points',
                'Total 3-points', 'Total Personal fouls']
    data = {}
    data['Player Name'] = player_name

    lines = clean_text_and_remove_excess(text)
    if not lines:
        for i in range(len(sections)):
            if sections[i] == 'Avg Minutes':
                data[sections[i]] = '00:00'
            elif sections[i] == 'Free throws percentage':
                data[sections[i]] = '0%'
            else:
                data[sections[i]] = '0'
        return data

    print("Lines after cleaning: ", lines)

    check_data(lines)

    for i in range(len(lines)):
        if i < len(sections):
            data[sections[i]] = lines[i]

    # Fill any missing sections with empty strings
    for section in sections:
        if section not in data:
            data[section] = ''

    return data


def extract_player_name(filename):
    # Assuming filename format is PlayerName_image.png
    base_name = os.path.splitext(filename)[0]  # Remove extension
    return base_name  # Adjust if your filename has different formatting
