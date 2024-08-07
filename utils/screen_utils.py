# File: screen_utils.py
# Path: utils\screen_utils.py

import mss
import datetime
import os
from PIL import Image
import cv2
import numpy as np
import pytesseract
import win32gui
from utils.my_logger import setup_logger

logger = setup_logger(__name__)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def calculate_relative_coords(rel_x, rel_y, rel_width, rel_height):
    def calculate(hwnd):
        try:
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]

            x = int(rel_x * width)
            y = int(rel_y * height)
            w = int(rel_width * width)
            h = int(rel_height * height)

            return x, y, w, h
        except Exception as e:
            logger.error(f"상대 좌표 계산 중 오류 발생: {e}")
            return None

    return calculate


def save_image(image, prefix=''):
    if not os.path.exists('debug_images'):
        os.makedirs('debug_images')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'debug_images/{prefix}_{timestamp}.png'

    try:
        if isinstance(image, Image.Image):
            image.save(filename)
        elif isinstance(image, np.ndarray):
            if image.ndim == 2:
                cv2.imwrite(filename, image)
            elif image.ndim == 3 and image.shape[2] == 3:
                cv2.imwrite(filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            else:
                cv2.imwrite(filename, image)
        else:
            raise ValueError("지원되지 않는 이미지 형식")

        logger.info(f"디버그 이미지 저장: {filename}")
    except Exception as e:
        logger.error(f"이미지 저장 중 오류 발생: {e}")

    return filename


def capture_window(hwnd, x, y, width, height):
    try:
        rect = win32gui.GetWindowRect(hwnd)
        left, top, _, _ = rect

        with mss.mss() as sct:
            monitor = {
                "top": top + y,
                "left": left + x,
                "width": width,
                "height": height
            }
            screenshot = sct.grab(monitor)
            img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
            save_image(img, 'raw_screenshot')  # PIL Image 저장
            img_np = np.array(img)
            return img_np, (x, y)
    except Exception as e:
        logger.error(f"윈도우 캡처 중 오류 발생: {e}")
        return None, None


def preprocess_image(image):
    if image is None or not isinstance(image, np.ndarray):
        logger.error("유효하지 않은 입력 이미지")
        raise ValueError("유효하지 않은 입력 이미지")

    try:
        opencv_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        save_image(gray, 'gray')

        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        save_image(denoised, 'denoised')

        binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        save_image(binary, 'binary')

        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        save_image(opening, 'opening')

        logger.info(f"전처리된 이미지 타입: {type(opening)}")
        logger.info(f"전처리된 이미지 크기: {opening.shape}")

        return opening
    except Exception as e:
        logger.error(f"이미지 전처리 중 오류 발생: {e}")
        return None


def extract_text(image, custom_config):
    try:
        save_image(image, 'before_ocr')  # OCR 전 이미지 저장
        ocr_data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
        logger.info("OCR 처리가 완료되었습니다.")
        return ocr_data
    except Exception as e:
        logger.error(f"OCR 처리 중 오류 발생: {e}")
        return None
