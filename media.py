import ctypes
import time
import pyautogui
import win32gui
import win32con
import pygetwindow as gw  # Assuming you have pygetwindow installed
from PIL import Image
import os

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


def move_mouse_to_player(hwnd, n, left, top, right, bottom):
    player_offset = (n-1) * (bottom - top) // 9 #TODO find offset

    # Move the mouse to the middle of the window
    pyautogui.moveTo(left + (right - left) // 6, top + (bottom - top) // 2 + player_offset)
    time.sleep(2)

    # Click the mouse
    pyautogui.click()
    time.sleep(2)

    move_to_player_stats(bottom, left, right, top)


def move_to_player_stats(bottom, left, right, top):
    # Now go to the middle of the windows width and at 1/6 of the height
    pyautogui.moveTo(left + (right - left) // 2, top + (bottom - top) // 8)
    time.sleep(2)
    # Click the mouse
    pyautogui.click()
    time.sleep(2)
    # Now go to the middle of the windows width and at 2/3 of the height
    pyautogui.moveTo(left + (right - left) // 2, top + 2 * (bottom - top) // 3)
    time.sleep(6)
    # Now grab and drag the mouse to the left of the window, at 2/3 of the height
    pyautogui.dragTo(left + (right - left) // 6, top + 2 * (bottom - top) // 3, 2, button='left')


def click_back_button(bottom, left, right, top):
    # Move the mouse to the top-left corner of the window, 1/10 of the width and 1/10 of the height
    pyautogui.moveTo(left + (right - left) // 14, top + (bottom - top) // 12)
    time.sleep(1)
    # Click the mouse
    pyautogui.click()
    time.sleep(2)


def slide_next_player(bottom, left, right, top):
    # Move the mouse to the last player
    print("Moving to the next player")
    player_offset = 4 * (bottom - top) // 9
    point_last_player(bottom, left, right, top)
    time.sleep(1)

    # Slide up 2/15 of the height, in the same x position
    pyautogui.dragTo(left + (right - left) // 6, top + (bottom - top) // 2 + player_offset - 5* (bottom - top) // 39, 1, button='left')
    time.sleep(2)


def point_last_player(bottom, left, right, top):
    player_offset = 4 * (bottom - top) // 9
    pyautogui.moveTo(left + (right - left) // 6, top + (bottom - top) // 2 + player_offset)

def get_team_stats_photo(bottom, left, right, top, folder_path):
    # Take a screenshot of the region corresponding to the window
    time.sleep(2)
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # Save the screenshot
    file_path = f"{folder_path}/GENERAL_STATS_temp.png"
    screenshot.save(file_path)




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
            move_mouse_to_player(hwnd,i, left, top, right, bottom)
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

def take_screenshot(bottom, left, right, top, folder_path):
    # Take a screenshot of the region corresponding to the window
    time.sleep(0.5)
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # Save the screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = f"{folder_path}/Screenshot_{timestamp}.png"
    screenshot.save(file_path)

