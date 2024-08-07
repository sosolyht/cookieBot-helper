# File: foreground.py
# Path: utils\foreground.py

import win32gui
import win32process
import psutil
from utils.my_logger import setup_logger

logger = setup_logger(__name__)

def bring_window_to_foreground(hwnd):
    try:
        if not win32gui.IsWindow(hwnd):
            logger.error("유효하지 않은 윈도우 핸들입니다.")
            return None

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        if not psutil.pid_exists(pid):
            logger.error(f"PID {pid}를 가진 프로세스를 찾을 수 없습니다.")
            return None

        logger.info(f"핸들 {hwnd}을 가진 창을 포그라운드로 가져오는 중입니다.")

        try:
            win32gui.SetForegroundWindow(hwnd)
            logger.info(f"핸들 {hwnd}을 가진 창이 이제 포그라운드에 있습니다.")
        except Exception as e:
            logger.error(f"포그라운드 창 설정 실패: {e}")
            return None

        return hwnd

    except Exception as e:
        logger.error(f"bring_window_to_foreground에서 오류 발생: {e}")
        return None
