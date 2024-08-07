# screen_utils.py
import mss
import datetime
import os
from PIL import Image
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import win32gui


def calculate_relative_coords(rel_x, rel_y, rel_width, rel_height):
    def calculate(hwnd):
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top

        actual_x = int(rel_x * width)
        actual_y = int(rel_y * height)
        actual_width = int(rel_width * width)
        actual_height = int(rel_height * height)

        return actual_x, actual_y, actual_width, actual_height

    return calculate


def capture_window(hwnd, x, y, width, height):
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

        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        # 파일 이름 생성 (현재 시간 기반)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join('screenshots', f'screenshot_{timestamp}.png')

        # 이미지 저장
        img.save(file_path)
        print(f"Screenshot saved to {file_path}")

        return img, (x, y)


def preprocess_image(image):
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
    _, thresh = cv2.threshold(sharpen, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return Image.fromarray(thresh)


def extract_text(image, custom_config):
    return pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
