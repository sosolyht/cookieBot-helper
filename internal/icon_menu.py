# File: icon_menu.py
# Path: internal\icon_menu.py

import time
import win32gui
import cv2
import numpy as np
import mss
import pyautogui
import ctypes
from PIL import Image
from utils.foreground import bring_window_to_foreground
from utils.my_logger import setup_logger

# 로거 설정
logger = setup_logger("IconMenu")


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


def find_button_advanced(screenshot, button_images, threshold=0.5):
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    best_match, best_value, best_size = None, -1, None

    for idx, img_path in enumerate(button_images):
        template = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            logger.error(f"이미지를 불러오지 못했습니다: {img_path}")
            continue

        h, w = template.shape[:2]
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        logger.debug(f"버튼: {img_path}, 최대 값: {max_val}")

        if max_val > best_value:
            best_value = max_val
            best_match = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            best_size = (w, h)

    if best_value > threshold:
        logger.info(f"최고 매치: 값={best_value}, 위치={best_match}")
        return best_match, best_size
    else:
        logger.warning(f"좋은 매치를 찾지 못했습니다. 최고 값: {best_value}")
        return None, None

def get_click_coordinates(hwnd, location):
    rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    left, top, _, _ = rect
    _, _, client_right, client_bottom = client_rect

    border_left = (rect[2] - rect[0] - client_right) // 2
    title_bar = rect[3] - rect[1] - client_bottom - border_left

    click_x = left + border_left + location[0]
    click_y = top + title_bar + location[1]

    return click_x, click_y

def icon_menu(hwnd, button_images):
    logger.info("아이콘 메뉴 처리 시작")
    bring_window_to_foreground(hwnd)
    time.sleep(1)

    screenshot = capture_client_area(hwnd)
    location, size = find_button_advanced(screenshot, button_images, threshold=0.5)

    if location:
        click_x, click_y = get_click_coordinates(hwnd, location)
        logger.info(f"버튼 위치 확인: ({click_x}, {click_y}), 크기: {size}")

        pyautogui.moveTo(click_x, click_y)
        time.sleep(0.5)

        screenshot = capture_client_area(hwnd)
        new_location, new_size = find_button_advanced(screenshot, button_images, threshold=0.5)
        if new_location:
            click_x, click_y = get_click_coordinates(hwnd, new_location)
            logger.info(f"버튼 위치 재확인: ({click_x}, {click_y}), 크기: {new_size}")

        logger.info(f"클릭 시도: ({click_x}, {click_y})")
        pyautogui.click(click_x, click_y)

        logger.info("아이콘 메뉴 클릭 성공")
        return True
    else:
        logger.warning("버튼을 찾을 수 없습니다.")
        return False