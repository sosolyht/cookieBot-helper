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


def save_image(image, name):
    try:
        # debug 폴더가 없으면 생성
        if not os.path.exists('debug'):
            os.makedirs('debug')

        path = os.path.join('debug', f"{name}.png")

        if isinstance(image, np.ndarray):
            Image.fromarray(image).save(path)
        elif isinstance(image, Image.Image):
            image.save(path)
        logger.info(f"{name} 이미지 저장 완료: {path}")
    except Exception as e:
        logger.error(f"{name} 이미지 저장 중 오류 발생: {e}")


def preprocess_image(image):
    try:
        # OpenCV 이미지로 변환
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 그레이스케일 변환
        gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)

        # 노이즈 제거
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)

        # 샤프닝
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(denoised, -1, sharpen_kernel)

        # 이진화
        _, thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        return Image.fromarray(thresh)
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return None


def capture_window(hwnd, x, y, width, height):
    try:
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect

        # 윈도우 너비의 10%만큼 오른쪽으로 이동 (이전 20%에서 변경)
        window_width = right - left
        left_margin = int(window_width * 0.10)  # 10% 여백으로 변경

        with mss.mss() as sct:
            monitor = {
                "top": top + y,
                "left": left + x + left_margin,  # 왼쪽 여백 추가
                "width": width,
                "height": height
            }
            screenshot = sct.grab(monitor)
            img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
            save_image(img, 'raw_screenshot')  # PIL Image 저장
            img_np = np.array(img)
            return img_np, (x + left_margin, y)  # 수정된 x 좌표 반환
    except Exception as e:
        logger.error(f"윈도우 캡처 중 오류 발생: {e}")
        return None, None


def extract_text(image, custom_config):
    try:
        save_image(image, 'before_ocr')  # OCR 전 이미지 저장
        ocr_data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
        logger.info("OCR 처리가 완료되었습니다.")
        return ocr_data
    except Exception as e:
        logger.error(f"OCR 처리 중 오류 발생: {e}")
        return None
