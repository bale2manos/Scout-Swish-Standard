import os
import cv2
import pytesseract
from PIL import Image
import pandas as pd


def preprocess_image(image_path):
    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Define rectangle properties
    rects = [
        ((0, 0), (image.shape[1] // 2, image.shape[0] // 3)),
        ((0, 0), (image.shape[1] // 5, image.shape[0])),
        ((0, image.shape[0] // 3), (image.shape[1], image.shape[0] // 3 + image.shape[0] // 3)),
    ]

    # Draw rectangles on the original image
    for (top_left, bottom_right) in rects:
        cv2.rectangle(image, top_left, bottom_right, 255, thickness=cv2.FILLED)
    
    # Invert colors if needed
    inverted_image = cv2.bitwise_not(image)
    
    # Save the image with the rectangles
    #cv2.imwrite('inverted_image_with_rectangle.png', inverted_image)

    # Resize for better OCR accuracy
    scaled_image = cv2.resize(inverted_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    #cv2.imwrite('scaled_image_with_rectangle.png', scaled_image)

    return scaled_image

def extract_text(image):
    image_pil = Image.fromarray(image)
    custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789.:%'
    
    extracted_text = pytesseract.image_to_string(image_pil, config=custom_config)

    return extracted_text

def extract_data_from_text(text, player_name):
    lines = text.split('\n')
    lines = clean_text_and_remove_excess(text)


    check_minutes(lines)
    check_over_50_points(lines)
    
    check_over_30_FT(lines)
    
    check_over_20_2FG(lines)
    
    check_over_20_3P(lines)
    
    check_over_5_PF(lines)

    lines = lines[:-1]  

    sections = ['Total Games', 'Avg Minutes', 'Avg Points', 'Avg Free throws', 'Avg 2-points', 'Avg 3-points', 'Avg Personal fouls',
                'Total Minutes', 'Total Points', 'Total Free throws', 'Free throws percentage', 'Total 2-points', 'Total 3-points', 'Total Personal fouls']
    
    data = {}
    data['Player Name'] = player_name
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

    # Remove points because they are repeated
    lines.pop(1)

    # Join lines into one string
    text = '\n'.join(lines)
    if '%\n' not in lines:
        lines = text.replace('%', '%\n')
    lines = lines.split('\n')
    lines = [line for line in lines if line]
    return lines

def check_over_5_PF(lines):
    if float(lines[6]) > 5:
        # Add a decimal point after the first character
        lines[6] = lines[6][:1] + '.' + lines[6][1:]

def check_over_20_3P(lines):
    if float(lines[5]) > 20:
        # Add a decimal point after the first character
        lines[5] = lines[5][:1] + '.' + lines[5][1:]

def check_over_20_2FG(lines):
    if float(lines[4]) > 20:
        # Add a decimal point after the first character
        lines[4] = lines[4][:1] + '.' + lines[4][1:]

def check_over_30_FT(lines):
    if float(lines[3]) > 30:
        # Add a decimal point after the first character
        lines[3] = lines[3][:1] + '.' + lines[3][1:]

def check_over_50_points(lines):
    if float(lines[2]) > 50:
        # Add a decimal point after the first character
        lines[2] = lines[2][:1] + '.' + lines[2][1:]

def check_minutes(lines):
    if ':' not in lines[1]:
        # After the first two chars, add the colon
        lines[1] = lines[1][:2] + ':' + lines[1][2:]
        # After the fifth char, add the following numbers to the next line
        lines.insert(2, lines[1][5:])
        # Remove the numbers from the first line
        lines[1] = lines[1][:5]

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
    df = pd.DataFrame(data)
    # Convert 'Avg Minutes' and 'Total Minutes' to numeric values
    df['Sort Minutes'] = df['Avg Minutes'].apply(time_to_seconds)
    df['Avg Points'] = pd.to_numeric(df['Avg Points'], errors='coerce')
    
    # Sort by 'Avg Points'
    df_sorted = df.sort_values(by='Avg Points', ascending=False)
    
    # Find the player with the most minutes, and remove the 'Sort Minutes' column
    most_minutes_player_idx = df_sorted['Sort Minutes'] .idxmax()

    df_sorted.drop(columns=['Sort Minutes'], inplace=True)
    df_sorted.at[most_minutes_player_idx, 'Relevant Info'] = 'MOST MINUTES'

    # Find the player with the most games played, if there are multiple players with the same number of games, all of them will be marked as 'MOST GAMES'
    most_games_player_idx = df_sorted['Total Games'].idxmax()
    most_games = df_sorted.at[most_games_player_idx, 'Total Games']
    for idx, row in df_sorted.iterrows():
        if row['Total Games'] == most_games:
            df_sorted.at[idx, 'Relevant Info'] = 'MOST GAMES'

    # Save the sorted DataFrame to Excel
    df_sorted.to_excel(excel_filename, index=False, engine='openpyxl')


# Collect all data
data = []
folder = './Pintobasket'
for filename in os.listdir(folder):
    if filename.endswith('.PNG') or filename.endswith('.png'):
        image_path = os.path.join(folder, filename)
        preprocessed_image = preprocess_image(image_path)
        extracted_text = extract_text(preprocessed_image)
        player_data = extract_data_from_text(extracted_text, extract_player_name(filename))
        data.append(player_data)

# Save to Excel
save_to_excel(data, 'player_data.xlsx')
print('Data saved to player_data.xlsx')

