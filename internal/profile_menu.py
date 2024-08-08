# File: profile_menu.py
# Path: internal\profile_menu.py

import time
import pyautogui
import win32gui
import mss
import mss.tools
from utils.get_hwnd import get_hwnd
from utils.foreground import bring_window_to_foreground
from utils.aws_textract import aws_textract_helper
from utils.my_logger import setup_logger

logger = setup_logger(__name__)

START_PROFILE = "New Profile"
MENU_ITEMS = ["Overview", "Proxy", "Extensions", "Timezone", "WebRTC", "Geolocation", "Advanced", "Cookies", "Bookmarks"]

menu_coordinates = {}

def capture_screenshot(hwnd, save_path):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": right - left, "height": bottom - top}
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)
    return save_path

def get_menu_coordinates(hwnd):
    global menu_coordinates
    screenshot_path = "debug/window_screenshot.png"
    capture_screenshot(hwnd, screenshot_path)
    results = aws_textract_helper(screenshot_path, MENU_ITEMS + [START_PROFILE])

    rect = win32gui.GetWindowRect(hwnd)
    left, top = rect[:2]
    for text, text_left, text_top, text_width, text_height in results:
        normalized_text = text.lower()
        for menu_item in MENU_ITEMS + [START_PROFILE]:
            if normalized_text == menu_item.lower():
                click_x = left + text_left + text_width // 2
                click_y = top + text_top + text_height // 2
                menu_coordinates[menu_item] = (click_x, click_y)

    logger.info(f"메뉴 좌표 저장 완료: {menu_coordinates}")

def click_menu_item(hwnd, item):
    normalized_item = item.lower()
    for menu_item, coordinates in menu_coordinates.items():
        if menu_item.lower() == normalized_item:
            click_x, click_y = coordinates
            pyautogui.click(click_x, click_y)
            logger.info(f"'{menu_item}' 항목을 클릭했습니다: ({click_x}, {click_y})")
            time.sleep(0.5)
            return True
    logger.error(f"메뉴 항목을 찾을 수 없습니다: {item}")
    return False


def process_profile_menu():
    hwnd = get_hwnd()
    if not hwnd or not bring_window_to_foreground(hwnd):
        logger.error("윈도우를 찾을 수 없거나 포그라운드로 가져올 수 없습니다")
        return

    get_menu_coordinates(hwnd)

    if not any(click_menu_item(item) for item in MENU_ITEMS):
        if click_menu_item(START_PROFILE):
            time.sleep(0.5)
            get_menu_coordinates(hwnd)
            for item in MENU_ITEMS:
                click_menu_item(item)

    logger.info("프로필 메뉴 처리 완료")

def get_menu_item_coordinates(item):
    return menu_coordinates.get(item)

if __name__ == "__main__":
    process_profile_menu()
