# screen_utils.py
import mss
import datetime
import os
from PIL import Image
import cv2
import numpy as np
import pytesseract
import win32gui

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
            return None

    return calculate


def save_image(image, prefix=''):
    if not os.path.exists('debug_images'):
        os.makedirs('debug_images')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'debug_images/{prefix}_{timestamp}.png'

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
        raise ValueError("Unsupported image type")

    print(f"Saved debug image: {filename}")
    return filename


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
        save_image(img, 'raw_screenshot')  # PIL Image 저장
        img_np = np.array(img)
        return img_np, (x, y)


def preprocess_image(image):
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Invalid input image")

    # RGB to BGR 변환
    opencv_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 그레이스케일 변환
    gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    save_image(gray, 'gray')

    # 노이즈 제거
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    save_image(denoised, 'denoised')

    # 적응형 이진화
    binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    save_image(binary, 'binary')

    # 모폴로지 연산으로 글자 다듬기
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    save_image(opening, 'opening')

    print(f"Preprocessed image type: {type(opening)}")
    print(f"Preprocessed image shape: {opening.shape}")

    return opening


def extract_text(image, custom_config):
    save_image(image, 'before_ocr')  # OCR 전 이미지 저장
    return pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)