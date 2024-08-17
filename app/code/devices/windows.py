import ctypes
import time
import win32gui
import win32con
import pygetwindow as gw  # Assuming you have pygetwindow installed

from .move_mouse import move_mouse_to_player, click_back_button, slide_next_player, point_last_player
from ..devices.screenshots import get_team_stats_photo, take_screenshot


def get_window_rect(hwnd):
    # Get the window's rectangle coordinates
    rect = win32gui.GetWindowRect(hwnd)
    return rect


def bring_window_to_front(hwnd):
    # Restore and bring the window to the front
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # Bring the window to the foreground
    ctypes.windll.user32.ShowWindow(hwnd, 5)  # 5 is SW_SHOW
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    ctypes.windll.user32.SetFocus(hwnd)

    # Allow time for the window to come to the foreground
    time.sleep(1)


def screenshot_window_by_title(window_title, n_players, folder_path):
    # Get the window handle for the specified title
    hwnds = gw.getWindowsWithTitle(window_title)
    if hwnds:
        hwnd = hwnds[0]._hWnd  # Get the window handle

        # Get the window's coordinates and size
        rect = get_window_rect(hwnd)
        left, top, right, bottom = rect

        # Ensure the window is brought to the front
        bring_window_to_front(hwnd)

        # Get team stats
        get_team_stats_photo(bottom, left, right, top, folder_path)

        # Move the mouse to the top-left corner of the window
        i=1
        for i in range(1, min(n_players+1, 6)):
            print(f"Player {i}")
            move_mouse_to_player(hwnd, i, left, top, right, bottom)
            take_screenshot(bottom, left, right, top, folder_path)
            time.sleep(2)

            # Go back to the team window
            click_back_button(bottom, left, right, top)


        while i < n_players:
            print(f"Player {i}")
            slide_next_player(bottom, left, right, top)
            move_mouse_to_player(hwnd, 5, left, top, right, bottom)
            take_screenshot(bottom, left, right, top, folder_path)
            time.sleep(2)
            # Go back to the team window
            click_back_button(bottom, left, right, top)
            i+=1

        point_last_player(bottom, left, right, top)


    else:
            print(f"Window with title '{window_title}' not found.")

