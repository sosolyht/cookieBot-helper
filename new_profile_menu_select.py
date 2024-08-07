import win32gui
import time
import pyautogui
import logging
from screen_utils import calculate_relative_coords, capture_window, preprocess_image, extract_text, save_image
from utils.foreground import bring_window_to_foreground

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_and_click(image, hwnd, offset, target_text):
    try:
        custom_config = r'--oem 3 --psm 6 -l eng -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        data = extract_text(image, custom_config)

        logger.info("Extracted text data:")
        for i in range(len(data['level'])):
            logger.info(f"Text: {data['text'][i]}, Confidence: {data['conf'][i]}, Position: ({data['left'][i]}, {data['top'][i]})")

        for i in range(len(data['level'])):
            if int(data['conf'][i]) > 0 and data['text'][i] == target_text:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                logger.info(f"Found '{target_text}' at: ({x}, {y}, {w}, {h}) in image coordinates")

                click_x = x + w // 2
                click_y = y + h // 2

                rect = win32gui.GetWindowRect(hwnd)
                left, top, _, _ = rect
                actual_click_x = left + offset[0] + click_x
                actual_click_y = top + offset[1] + click_y

                logger.info(f"Clicking at: ({actual_click_x}, {actual_click_y})")
                try:
                    pyautogui.click(actual_click_x, actual_click_y)
                except Exception as e:
                    logger.error(f"Failed to click: {e}")
                    return False
                return True
        logger.info(f"'{target_text}' text not found in the image.")
        return False
    except Exception as e:
        logger.error(f"Error in extract_text_and_click: {e}")
        return False


def click_menu_item(hwnd, menu_item):
    if hwnd is None:
        logger.error("Invalid window handle.")
        return False

    try:
        logger.info(f"Using window with HWND: {hwnd}")

        hwnd = bring_window_to_foreground(hwnd)
        if not hwnd or not win32gui.IsWindow(hwnd):
            logger.error("Failed to bring the window to foreground or invalid window handle.")
            return False

        time.sleep(1)

        calculate_coords = calculate_relative_coords(50 / 1366, 76 / 768, 300 / 1366, 614 / 768)
        coords = calculate_coords(hwnd)
        if coords is None:
            logger.error("Failed to calculate coordinates.")
            return False

        x, y, width, height = coords
        screenshot, offset = capture_window(hwnd, x, y, width, height)

        save_image(screenshot, 'screenshot_before_preprocess')

        preprocessed_image = preprocess_image(screenshot)

        logger.info(f"Extracting text and clicking on '{menu_item}' from the preprocessed screenshot...")
        if not extract_text_and_click(preprocessed_image, hwnd, offset, menu_item):
            logger.error(f"'{menu_item}' text not found in the image.")
            return False
        return True

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False