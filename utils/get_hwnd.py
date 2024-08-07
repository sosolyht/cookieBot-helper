import ctypes
import ctypes.wintypes
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

user32 = ctypes.windll.user32

def get_hwnd():
    target_title = "Hidemyacc 3.0.69"
    found_hwnd = [None]

    def enum_windows_callback(hwnd, lParam):
        try:
            if user32.IsWindowVisible(hwnd):
                print(f"Window {hwnd} is visible.")
                length = user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                print(f"Window title: {buff.value}")
                if buff.value == target_title:
                    found_hwnd[0] = hwnd
                    logger.info(f"Found window with title '{target_title}' and HWND: {hwnd}")
                    return False  # Stop enumeration
        except Exception as e:
            logger.error(f"Error in enum_windows_callback: {e}")
        return True

    try:
        print("Starting window enumeration...")
        enum_windows_prototype = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.c_void_p)
        enum_windows_func = enum_windows_prototype(enum_windows_callback)
        user32.EnumWindows(enum_windows_func, 0)
        print("Finished window enumeration.")
    except Exception as e:
        logger.error(f"Error during window enumeration: {e}")

    print(f"Found HWND: {found_hwnd[0]}")
    return found_hwnd[0]

if __name__ == "__main__":
    try:
        hwnd = get_hwnd()
        if hwnd:
            logger.info(f"Found Hidemyacc 3.0.69 with HWND: {hwnd}")
        else:
            logger.warning("Hidemyacc 3.0.69 not found")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
