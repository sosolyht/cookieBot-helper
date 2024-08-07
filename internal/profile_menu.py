# File: profile_menu.py
# Path: internal\profile_menu.py

import time
import os
import pyautogui
import win32gui
from utils.get_hwnd import get_hwnd
from utils.foreground import bring_window_to_foreground
from utils.screen_utils import save_image
from utils.aws_textract import aws_textract_helper
from utils.my_logger import setup_logger

# 로거 설정
logger = setup_logger(__name__)

MENU_ITEMS = [
    "Overview",
    "Proxy",
    "Extensions",
    "Timezone",
    "WebRTC",
    "Geolocation",
    "Advanced",
    "Cookies",
    "Bookmarks"
]

def capture_screenshot_of_window(save_path):
    try:
        hwnd = get_hwnd()
        if hwnd is None:
            logger.error("지정된 창을 찾을 수 없습니다.")
            return None

        if bring_window_to_foreground(hwnd):
            time.sleep(1)

            rect = win32gui.GetWindowRect(hwnd)
            left, top, right, bottom = rect
            width = right - left
            height = bottom - top

            screenshot = pyautogui.screenshot(region=(left, top, width, height))

            save_path = os.path.abspath(save_path)

            save_dir = os.path.dirname(save_path)
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir)

            base, ext = os.path.splitext(save_path)
            if ext.lower() != '.png':
                save_path = base + '.png'

            save_image(screenshot, save_path)
            logger.info(f"스크린샷이 {save_path}에 저장되었습니다.")

            return save_path
        else:
            logger.error("창을 포그라운드로 가져오지 못했습니다.")
            return None

    except Exception as e:
        logger.error(f"스크린샷 캡처 중 오류 발생: {e}")
        return None

def process_profile_menu():
    logger.info("프로필 메뉴 처리 시작")
    screenshot_path = "debug/window_screenshot.png"
    screenshot_absolute_path = capture_screenshot_of_window(screenshot_path)

    if screenshot_absolute_path and os.path.exists(screenshot_absolute_path):
        results = aws_textract_helper(screenshot_absolute_path, MENU_ITEMS)

        hwnd = get_hwnd()
        if hwnd is None:
            logger.error("지정된 창을 찾을 수 없습니다.")
            return

        if bring_window_to_foreground(hwnd):
            time.sleep(1)

            rect = win32gui.GetWindowRect(hwnd)
            left, top, right, bottom = rect
            window_width = right - left
            window_height = bottom - top

            for result in results:
                text, text_left, text_top, text_width, text_height = result
                logger.info(f"텍스트: {text}")
                logger.info(f"위치: Left={text_left}, Top={text_top}, Width={text_width}, Height={text_height}")

                click_x = left + text_left + text_width // 2
                click_y = top + text_top + text_height // 2

                pyautogui.click(click_x, click_y)
                logger.info(f"Clicked at: ({click_x}, {click_y})")

                time.sleep(0.5)

        else:
            logger.error("창을 포그라운드로 가져오지 못했습니다.")
    else:
        logger.error(f"스크린샷 파일이 존재하지 않습니다: {screenshot_absolute_path}")

    logger.info("프로필 메뉴 처리 완료")

if __name__ == "__main__":
    process_profile_menu()
