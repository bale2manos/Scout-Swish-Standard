import time

import pyautogui


def get_team_stats_photo(bottom, left, right, top, folder_path):
    # Take a screenshot of the region corresponding to the window
    time.sleep(2)
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # Save the screenshot
    file_path = f"{folder_path}/GENERAL_STATS_temp.png"
    screenshot.save(file_path)


def take_screenshot(bottom, left, right, top, folder_path):
    # Take a screenshot of the region corresponding to the window
    time.sleep(0.5)
    screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

    # Save the screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = f"{folder_path}/Screenshot_{timestamp}.png"
    screenshot.save(file_path)
