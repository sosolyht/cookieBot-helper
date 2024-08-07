# File: get_hwnd.py
# Path: utils\get_hwnd.py

import ctypes
import ctypes.wintypes
from utils.my_logger import setup_logger

logger = setup_logger(__name__)

user32 = ctypes.windll.user32

def get_hwnd():
    target_title = "Hidemyacc 3.0.69"
    found_hwnd = [None]

    def enum_windows_callback(hwnd, lParam):
        try:
            if user32.IsWindowVisible(hwnd):
                logger.debug(f"윈도우 {hwnd}가 보입니다.")
                length = user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                logger.debug(f"윈도우 제목: {buff.value}")
                if buff.value == target_title:
                    found_hwnd[0] = hwnd
                    logger.info(f"'{target_title}' 제목의 윈도우를 찾았습니다. HWND: {hwnd}")
                    return False  # 열거 중지
        except Exception as e:
            logger.error(f"enum_windows_callback에서 오류 발생: {e}")
        return True

    try:
        logger.info("윈도우 열거 시작...")
        enum_windows_prototype = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.c_void_p)
        enum_windows_func = enum_windows_prototype(enum_windows_callback)
        user32.EnumWindows(enum_windows_func, 0)
        logger.info("윈도우 열거 완료.")
    except Exception as e:
        logger.error(f"윈도우 열거 중 오류 발생: {e}")

    logger.info(f"찾은 HWND: {found_hwnd[0]}")
    return found_hwnd[0]

if __name__ == "__main__":
    try:
        hwnd = get_hwnd()
        if hwnd:
            logger.info(f"Hidemyacc 3.0.69을 찾았습니다. HWND: {hwnd}")
        else:
            logger.warning("Hidemyacc 3.0.69를 찾지 못했습니다.")
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {e}")
