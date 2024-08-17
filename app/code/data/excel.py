import pytesseract
import pandas as pd

from ..utils.utils import time_to_seconds

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'F:\Programas\Tesseract-OCR\tesseract.exe'


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
    print("Most minutes player index: ", most_minutes_player_idx)
    df_sorted.at[most_minutes_player_idx, 'Relevant Info'] = 'MOST MINUTES'


