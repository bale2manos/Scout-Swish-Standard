import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from code.media.process_image import process_images, get_team_stats
from code.media.image_to_text import get_player_name
from code.media.cropping import crop_image_to_second_third_row, crop_image_to_second_fifth_row
from code.devices.windows import screenshot_window_by_title



def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_selected)

def toggle_advanced_mode():
    if advanced_mode_var.get():
        window_title_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=10)
    else:
        window_title_frame.grid_forget()

def start_process():
    folder_path = folder_path_entry.get()
    n_players = int(players_entry.get())
    window_title = window_title_entry.get()

    if not folder_path or not n_players or not window_title:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Take screenshot
    screenshot_window_by_title(window_title, n_players, folder_path)

    # Create necessary directories
    if not os.path.exists(f'{folder_path}/Stats Cropped'):
        os.makedirs(f'{folder_path}/Stats Cropped')

    if not os.path.exists(f'{folder_path}/Results'):
        os.makedirs(f'{folder_path}/Results')

    # Process each image in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and filename != 'GENERAL_STATS_temp.png':
            image_path = os.path.join(folder_path, filename)
            try:
                player_name = get_player_name(image_path, f'{folder_path}/temp.png')
                player_stats_output_path = f'{folder_path}/Stats Cropped/{player_name}.png'
                crop_image_to_second_third_row(image_path, player_stats_output_path)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    # Process general stats and save
    crop_image_to_second_fifth_row(f'{folder_path}/GENERAL_STATS_temp.png', f'{folder_path}/Stats Cropped/GENERAL_STATS.png')
    team_stats = get_team_stats(f'{folder_path}/Stats Cropped/GENERAL_STATS.png')

    with open(f'{folder_path}/Results/Team Stats.txt', 'w') as f:
        for key, value in team_stats.items():
            f.write(f"{key}: {value}\n")

    process_images(f'{folder_path}/Stats Cropped', f'{folder_path}/Results/Players Stats.xlsx')

    messagebox.showinfo("Process Completed", "The process has been completed successfully.")

# Create main window
root = tk.Tk()
root.title("Basketball Stats Processor")

# Set initial window size and center it on the screen
window_width = 900
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position x, y for the window
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Set a light background color for the root window
root.configure(background='#F5F5F5')  # Light grey for a clean look

# Style configuration for ttk widgets
style = ttk.Style()
style.configure("TLabel", background='#F5F5F5', foreground='#333333', font=('Helvetica', 14))
style.configure("TEntry", padding=5, font=('Helvetica', 12))
style.configure("TButton", background='#141414', foreground='#141414', font=('Helvetica', 12, 'bold'), padding=10)
style.map("TButton", background=[('active', '#444444')])  # Darker on hover
style.configure("TFrame", background='#F5F5F5')  # Frame background color

# Title Label
title_label = ttk.Label(root, text="🏀 Basketball Stats Processor 🏀", font=('Helvetica', 20, 'bold'))
title_label.grid(row=0, column=0, columnspan=3, pady=20)

# Folder path
folder_path_label = ttk.Label(root, text="Select Folder:")
folder_path_label.grid(row=1, column=0, padx=20, pady=10)
folder_path_entry = ttk.Entry(root, width=50)
folder_path_entry.grid(row=1, column=1, padx=20, pady=10)
browse_button = ttk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2, padx=20, pady=10)

# Number of players
players_label = ttk.Label(root, text="Number of Players:")
players_label.grid(row=2, column=0, padx=20, pady=10)
players_entry = ttk.Entry(root, width=10)
players_entry.grid(row=2, column=1, padx=20, pady=10)

# Window title in advanced mode
advanced_mode_var = tk.BooleanVar()
advanced_check = ttk.Checkbutton(root, text="Advanced Mode", variable=advanced_mode_var, command=toggle_advanced_mode)
advanced_check.grid(row=3, column=0, columnspan=3, pady=10)

window_title_frame = ttk.Frame(root)
window_title_label = ttk.Label(window_title_frame, text="Window Title:")
window_title_label.grid(row=0, column=0, padx=20, pady=10)
window_title_entry = ttk.Entry(window_title_frame, width=50)
window_title_entry.grid(row=0, column=1, padx=20, pady=10)
window_title_entry.insert(0, "BlueStacks App Player")

# Start button
start_button = ttk.Button(root, text="Start Process", command=start_process)
start_button.grid(row=4, column=0, columnspan=3, pady=20)

# Adjust the root window size to fit all widgets
root.update_idletasks()  # Update "requested size" from all widgets
root.geometry(f"{root.winfo_reqwidth()}x{root.winfo_reqheight()+20}+{x_cordinate}+{y_cordinate}")

# Main loop
root.mainloop()
