import time

import pyautogui


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


def point_last_player(bottom, left, right, top):
    player_offset = 4 * (bottom - top) // 9
    pyautogui.moveTo(left + (right - left) // 6, top + (bottom - top) // 2 + player_offset)


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
