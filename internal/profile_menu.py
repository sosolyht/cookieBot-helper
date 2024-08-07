# File: profile_menu.py
# Path: internal\profile_menu.py

import win32gui
import time
import pyautogui
from utils.screen_utils import calculate_relative_coords, capture_window, preprocess_image, extract_text, save_image
from utils.foreground import bring_window_to_foreground
from utils.my_logger import setup_logger

logger = setup_logger(__name__)

def extract_text_and_click(image, hwnd, offset, target_text):
    try:
        custom_config = r'--oem 3 --psm 6 -l eng -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        data = extract_text(image, custom_config)

        logger.info("추출된 텍스트 데이터:")
        for i in range(len(data['level'])):
            logger.info(f"텍스트: {data['text'][i]}, 신뢰도: {data['conf'][i]}, 위치: ({data['left'][i]}, {data['top'][i]})")

        for i in range(len(data['level'])):
            if int(data['conf'][i]) > 0 and data['text'][i] == target_text:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                logger.info(f"'{target_text}' 찾음: 이미지 좌표 ({x}, {y}, {w}, {h})")

                click_x = x + w // 2
                click_y = y + h // 2

                rect = win32gui.GetWindowRect(hwnd)
                left, top, _, _ = rect
                actual_click_x = left + offset[0] + click_x
                actual_click_y = top + offset[1] + click_y

                logger.info(f"클릭 위치: ({actual_click_x}, {actual_click_y})")
                try:
                    pyautogui.click(actual_click_x, actual_click_y)
                except Exception as e:
                    logger.error(f"클릭 실패: {e}")
                    return False
                return True
        logger.info(f"'{target_text}' 텍스트를 이미지에서 찾지 못했습니다.")
        return False
    except Exception as e:
        logger.error(f"extract_text_and_click에서 오류 발생: {e}")
        return False

def click_menu_item(hwnd, menu_item):
    if hwnd is None:
        logger.error("잘못된 윈도우 핸들입니다.")
        return False

    try:
        logger.info(f"HWND를 사용 중: {hwnd}")

        hwnd = bring_window_to_foreground(hwnd)
        if not hwnd or not win32gui.IsWindow(hwnd):
            logger.error("윈도우를 포그라운드로 못 가져오거나 잘못된 윈도우 핸들입니다.")
            return False

        time.sleep(1)

        calculate_coords = calculate_relative_coords(50 / 1366, 76 / 768, 300 / 1366, 614 / 768)
        coords = calculate_coords(hwnd)
        if coords is None:
            logger.error("좌표 계산 실패.")
            return False

        x, y, width, height = coords
        screenshot, offset = capture_window(hwnd, x, y, width, height)

        save_image(screenshot, 'screenshot_before_preprocess')

        preprocessed_image = preprocess_image(screenshot)

        logger.info(f"전처리된 스크린샷에서 '{menu_item}' 텍스트를 추출하고 클릭 중...")
        if not extract_text_and_click(preprocessed_image, hwnd, offset, menu_item):
            logger.error(f"이미지에서 '{menu_item}' 텍스트를 찾지 못했습니다.")
            return False
        return True

    except Exception as e:
        logger.error(f"오류 발생: {e}")
        return False
