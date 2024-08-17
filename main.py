# main.py
import os
from stats import process_images, get_team_stats
from crop_image import get_player_name, crop_image_to_second_third_row, crop_image_to_second_fifth_row
from media import screenshot_window_by_title


def main():
    # Example usage of process_images
    folder_path = './Villa de Aranjuez - 2011 Fem'

    # Create a folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


    # Specify the window title to capture
    window_title = "BlueStacks App Player"
    n_players = 14 # TODO Change this to the input
    screenshot_window_by_title(window_title, n_players, folder_path)


    # Create a Stats folder if it doesn't exist
    if not os.path.exists(f'{folder_path}/Stats Cropped'):
        os.makedirs(f'{folder_path}/Stats Cropped')
    # Create a directory inside the folder called Results
    if not os.path.exists(f'{folder_path}/Results'):
        os.makedirs(f'{folder_path}/Results')

    # For every image in the folder
    for filename in os.listdir(folder_path):
        print("This is the filename: ", filename)
        if (filename.lower().endswith(('.png', '.jpg', '.jpeg')) and filename != 'GENERAL_STATS_temp.png'):
            image_path = os.path.join(folder_path, filename)
            try:
                print(f"Cropping {image_path}...")

                player_name = get_player_name(image_path, f'{folder_path}/temp.png')
                print(f"Player name: {player_name}")

                player_stats_output_path = f'{folder_path}/Stats Cropped/{player_name}.png'
                crop_image_to_second_third_row(image_path, player_stats_output_path)
                print(f"Player stats cropped and saved to {player_stats_output_path}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")


    # Process all images
    crop_image_to_second_fifth_row(f'{folder_path}/GENERAL_STATS_temp.png', f'{folder_path}/Stats Cropped/GENERAL_STATS.png')
    team_stats = get_team_stats(f'{folder_path}/Stats Cropped/GENERAL_STATS.png')

    # In team_stats there is a dictionary with the stats of the team, bulk them to a file in a readable format
    with open(f'{folder_path}/Results/Team Stats.txt', 'w') as f:
        for key, value in team_stats.items():
            f.write(f"{key}: {value}\n")

    stats_players_path = f'{folder_path}/Stats Cropped'
    excel_path = f'{folder_path}/Results/Players Stats.xlsx'
    process_images(stats_players_path, excel_path)

    print("Done!")


if __name__ == "__main__":
    main()
