import time
import win32gui
import cv2
import numpy as np
import mss
import pyautogui
import ctypes
from PIL import Image
from utils.foreground import bring_window_to_foreground


def capture_client_area(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    left, top, right, bottom = rect
    client_right, client_bottom = client_rect[2:]

    border_left = (right - left - client_right) // 2
    title_bar = bottom - top - client_bottom - border_left

    with mss.mss() as sct:
        monitor = {
            "top": top + title_bar,
            "left": left + border_left,
            "width": client_right,
            "height": client_bottom
        }
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
        return np.array(img)


def find_button_advanced(screenshot, button_images):
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    best_match, best_value, best_size = None, -1, None

    for idx, img_path in enumerate(button_images):
        template = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"Failed to load image: {img_path}")
            continue

        h, w = template.shape[:2]
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"Button: {img_path}, Max value: {max_val}")

        if max_val > best_value:
            best_value = max_val
            best_match = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            best_size = (w, h)

    if best_value > 0.7:
        print(f"Best match: value={best_value}, location={best_match}")
        return best_match, best_size
    else:
        print(f"No good match found. Best value: {best_value}")
        return None, None


def get_click_coordinates(hwnd, location):
    rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    left, top = rect[:2]
    client_right, client_bottom = client_rect[2:]

    border_left = (rect[2] - left - client_right) // 2
    title_bar = rect[3] - top - client_bottom - border_left

    dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
    scale_factor = dpi / 96.0

    button_x, button_y = location
    click_x = left + border_left + int(button_x / scale_factor)
    click_y = top + title_bar + int(button_y / scale_factor)

    return click_x, click_y


def click_button(hwnd, button_images):
    bring_window_to_foreground(hwnd)  # 윈도우를 전면으로 가져오기
    time.sleep(1)
    screenshot = capture_client_area(hwnd)
    location, _ = find_button_advanced(screenshot, button_images)

    if location:
        click_x, click_y = get_click_coordinates(hwnd, location)
        pyautogui.moveTo(click_x, click_y)
        time.sleep(0.5)

        # 위치 재확인
        screenshot = capture_client_area(hwnd)
        new_location, _ = find_button_advanced(screenshot, button_images)
        if new_location:
            click_x, click_y = get_click_coordinates(hwnd, new_location)

        print(f"Clicking at ({click_x}, {click_y})")
        pyautogui.click(click_x, click_y)
    else:
        print(f"Button not found.")
