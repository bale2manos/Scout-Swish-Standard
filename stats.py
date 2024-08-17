import os
from csv import excel

import cv2
import pytesseract
from PIL import Image
import pandas as pd

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'F:\Programas\Tesseract-OCR\tesseract.exe'

import cv2
import os
import shutil


# Define a mapping from special characters to their simpler equivalents
def simplify_path(path):
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


def preprocess_image(image_path):
    temp_path = create_temp_copy(image_path)

    # Read the image in grayscale from the new path
    image = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded properly
    if image is None:
        raise FileNotFoundError(
            f"Could not read image from {temp_path}. Please ensure the file exists and is accessible.")

    # Define rectangle properties
    rects = [
        ((0, 0), (image.shape[1] // 2, image.shape[0] // 3)),
        ((0, 0), (image.shape[1] // 5, image.shape[0])),
        ((0, image.shape[0] // 3), (image.shape[1], image.shape[0] // 3 + image.shape[0] // 3)),
    ]

    # Draw rectangles on the image
    for (top_left, bottom_right) in rects:
        cv2.rectangle(image, top_left, bottom_right, 255, thickness=cv2.FILLED)

    # Invert colors if needed
    inverted_image = cv2.bitwise_not(image)

    # Resize for better OCR accuracy
    scaled_image = cv2.resize(inverted_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


    # Optionally remove the temporary file if you no longer need it
    os.remove(temp_path)


    return scaled_image


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


def extract_text(image):
    image_pil = Image.fromarray(image)
    custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789.:%-'

    extracted_text = pytesseract.image_to_string(image_pil, config=custom_config)
    return extracted_text


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

    check_minutes(lines)
    check_over_40_points(lines)
    check_over_30_FT(lines)
    check_over_20_2FG(lines)
    check_over_20_3P(lines)
    check_over_5_PF(lines)
    check_over_50_over_under(lines)

    double_check_points(lines)




    for i in range(len(lines)):
        if i < len(sections):
            data[sections[i]] = lines[i]

    # Fill any missing sections with empty strings
    for section in sections:
        if section not in data:
            data[section] = ''

    return data


def clean_text_and_remove_excess(text):
    lines = text.split('\n')
    lines = [line for line in lines if line]

    print("Lines: ", lines)

    if lines[0] == '0':
        return

    # Remove points because they are repeated
    if len(lines) > 1:
        lines[3] = lines[1]
        lines.pop(1)

    # Join lines into one string
    text = '\n'.join(lines)
    if '%\n' not in text:
        text = text.replace('%', '%\n')
    lines = text.split('\n')
    lines = [line for line in lines if line]

    return lines

def check_over_50_over_under(lines):
    if len(lines) > 7 and float(lines[7]) > 50:
        # If number is over 100, add a decimal point after the second character, if  not add it after the first character
        if float(lines[7]) > 100:
            lines[7] = lines[7][:2] + '.' + lines[7][2:]
        else:
            lines[7] = lines[7][:1] + '.' + lines[7][1:]

def check_over_40_points(lines):
    if len(lines) > 2 and float(lines[2]) > 40:
        # Add a decimal point after the first character
        lines[2] = lines[2][:1] + '.' + lines[2][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 2 and len(lines[2]) > 1 and lines[2][0] == '0' and lines[2][1] != '.':
        lines[2] = lines[2][:1] + '.' + lines[2][1:]

def check_over_5_PF(lines):
    if len(lines) > 6 and float(lines[6]) > 5:
        # Add a decimal point after the first character
        lines[6] = lines[6][:1] + '.' + lines[6][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 6 and len(lines[6]) > 1 and lines[6][0] == '0' and lines[6][1] != '.':
        lines[6] = lines[6][:1] + '.' + lines[6][1:]


def check_over_20_3P(lines):
    if len(lines) > 5 and float(lines[5]) > 20:
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]
    elif len(lines) > 5 and float(lines[5]) * 3 > float(lines[2]):
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]
    elif len(lines) > 5 and float(lines[5]) * 3 == float(lines[2]) and (float(lines[4]) != 0 or float(lines[3]) != 0):
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 3 and len(lines[5]) > 1 and lines[5][0] == '0' and lines[5][1] != '.':
        lines[5] = lines[5][:1] + '.' + lines[5][1:]


def check_over_20_2FG(lines):
    if len(lines) > 4 and float(lines[4]) > 20:
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]
    elif len(lines) > 4 and float(lines[4]) * 2 > float(lines[2]):
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]
    elif len(lines) > 4 and float(lines[4]) * 2 == float(lines[2]) and (float(lines[3]) != 0 or float(lines[5]) != 0):
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 3 and len(lines[4]) > 1 and lines[4][0] == '0' and lines[4][1] != '.':
        lines[4] = lines[4][:1] + '.' + lines[4][1:]



def check_over_30_FT(lines):
    if len(lines) > 3 and float(lines[3]) > 30:
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]
    elif len(lines) > 3 and float(lines[3]) > float(lines[2]):
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]
        print("Free throws are over the total points")
    elif len(lines) > 3 and float(lines[3]) == float(lines[2]) and (float(lines[4]) != 0 or float(lines[5]) != 0):
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]
        print("Free throws are equal to the total points")

    # If the number has more than 1 digit and starts with 0, add a decimal point after the first character
    if len(lines) > 3 and len(lines[3]) > 1 and lines[3][0] == '0' and lines[3][1] != '.':
        lines[3] = lines[3][:1] + '.' + lines[3][1:]





def check_minutes(lines):
    if len(lines) > 1 and ':' not in lines[1]:
        # After the first two chars, add the colon
        lines[1] = lines[1][:2] + ':' + lines[1][2:]
        # After the fifth char, add the following numbers to the next line
        lines.insert(2, lines[1][5:])
        # Remove the numbers from the first line
        lines[1] = lines[1][:5]

def double_check_points(lines):
    if len(lines) > 5:
        free_throws_pts = float(lines[3]) * 1
        two_points_pts = float(lines[4]) * 2
        three_points_pts = float(lines[5]) * 3
        total_points = float(lines[2])
        # I want to check if the points match but give a certain amount of possible error, up to 1 point
        if abs(free_throws_pts + two_points_pts + three_points_pts - total_points) > 1:
            print("Points don't match")
            print(f"Free throws: {free_throws_pts}, 2 points: {two_points_pts}, 3 points: {three_points_pts}, total: {total_points}")
            # Add a decimal point after the first character
            lines[2] = lines[2][:1] + '.' + lines[2][1:]




def time_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    except ValueError:
        return 0


def extract_player_name(filename):
    # Assuming filename format is PlayerName_image.png
    base_name = os.path.splitext(filename)[0]  # Remove extension
    return base_name  # Adjust if your filename has different formatting

def save_to_excel(data, excel_filename):
    if not data:
        print("No data to save.")
        return

    df = pd.DataFrame(data)
    print("Data collected for saving:")
    print(df.head())

    # print colymn Free throws percentage
    print(df['Free throws percentage'])

    df['Avg Points'] = pd.to_numeric(df['Avg Points'], errors='coerce')

    # Process 'Free throws percentage' column
    df['Free throws percentage'] = df['Free throws percentage'].str.replace('%', '').astype(float) / 100

    # Sort by 'Avg Points'
    df_sorted = df.sort_values(by='Avg Points', ascending=False)

    find_player_most_minutes(df, df_sorted)
    find_player_most_games(df_sorted)

    # Convert all columns, besides Player Name, Avg Minutes, and Relevant Info, to numeric
    convert_to_numeric = df_sorted.columns.difference(
        ['Player Name', 'Avg Minutes', 'Relevant Info', 'Free throws percentage'])
    df_sorted[convert_to_numeric] = df_sorted[convert_to_numeric].apply(pd.to_numeric, errors='coerce')

    # Save the DataFrame to Excel without rounding
    df_sorted.to_excel(excel_filename, index=False)

    # Load the Excel file to apply percentage formatting to the 'Free throws percentage' column
    with pd.ExcelWriter(excel_filename, engine='openpyxl', mode='a') as writer:
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        percent_col_idx = df_sorted.columns.get_loc('Free throws percentage') + 1  # Excel is 1-indexed
        for cell in worksheet[worksheet.cell(1, percent_col_idx).column_letter]:
            cell.number_format = '0.00%'

    print(f"Data saved to {excel_filename}")


def find_player_most_games(df_sorted):
    # Find the player with the most games played, if there are multiple players with the same number of games, all of them will be marked as 'MOST GAMES'
    # First convert the 'Total Games' column to numeric
    df_sorted['Total Games'] = pd.to_numeric(df_sorted['Total Games'], errors='coerce')
    most_games_players_idx = df_sorted[df_sorted['Total Games'] == df_sorted['Total Games'].max()].index
    # If for that/those players the 'Relevant Info' column is already filled, append 'MOST GAMES' to it
    for idx in most_games_players_idx:
        if pd.notna(df_sorted.at[idx, 'Relevant Info']):
            df_sorted.at[idx, 'Relevant Info'] += ', MOST GAMES'
        else:
            df_sorted.at[idx, 'Relevant Info'] = 'MOST GAMES'


def find_player_most_minutes(df, df_sorted):
    df_sorted['Sort Minutes'] = df['Avg Minutes'].apply(time_to_seconds)
    # Find the player with the most minutes, and remove the 'Sort Minutes' column
    most_minutes_player_idx = df_sorted['Sort Minutes'].idxmax()
    df_sorted.drop(columns=['Sort Minutes'], inplace=True)
    df_sorted.at[most_minutes_player_idx, 'Relevant Info'] = 'MOST MINUTES'


def process_images(folder_path, excel_path):
    data = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and filename != 'GENERAL_STATS.png':
            image_path = os.path.join(folder_path, filename)
            try:
                print(f"Processing {image_path}...")
                preprocessed_image = preprocess_image(image_path)
                text = extract_text(preprocessed_image)
                player_name = extract_player_name(filename)
                player_data = extract_data_from_text(text, player_name)
                if player_data:
                    data.append(player_data)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    save_to_excel(data, excel_path)

def get_team_stats(image_path):
    # Open the image file, read the text and return it
    preprocessed_image = preprocess_image(image_path)

    # Read the image in grayscale from the new path
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded properly
    if image is None:
        raise FileNotFoundError(
            f"Could not read image from {image_path}. Please ensure the file exists and is accessible.")

    # Invert colors if needed
    inverted_image = cv2.bitwise_not(image)

    # Resize for better OCR accuracy
    scaled_image = cv2.resize(inverted_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    text = extract_text(scaled_image)

    lines = text.split('\n')
    lines = [line for line in lines if line]
    sections = ['Wins', 'Loses', 'Avg Points Scored', 'Avg Points Received']
    data = {}
    for i in range(len(lines)):
        if i < len(sections):
            data[sections[i]] = lines[i]

    print(data)
    return data
