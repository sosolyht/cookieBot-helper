# File: foreground.py
# Path: utils\foreground.py

import win32gui
import win32process
import win32com.client
import psutil
import time
from utils.my_logger import setup_logger

logger = setup_logger(__name__)

def bring_window_to_foreground(hwnd):
    try:
        if not win32gui.IsWindow(hwnd):
            logger.error("유효하지 않은 윈도우 핸들입니다.")
            return False

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        if not psutil.pid_exists(pid):
            logger.error(f"PID {pid}를 가진 프로세스를 찾을 수 없습니다.")
            return False

        logger.info(f"핸들 {hwnd}을 가진 창을 포그라운드로 가져오는 중입니다.")

        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')

        try:
            win32gui.ShowWindow(hwnd, 9)  # SW_RESTORE
            win32gui.SetForegroundWindow(hwnd)
        except Exception as e:
            logger.error(f"포그라운드 창 설정 실패: {e}")
            return False

        # 창이 실제로 포그라운드로 왔는지 확인
        for _ in range(10):  # 최대 1초 동안 시도
            if win32gui.GetForegroundWindow() == hwnd:
                logger.info(f"핸들 {hwnd}을 가진 창이 이제 포그라운드에 있습니다.")
                return True
            time.sleep(0.1)

        logger.warning(f"핸들 {hwnd}을 가진 창을 포그라운드로 가져오는 데 실패했습니다.")
        return False

    except Exception as e:
        logger.error(f"bring_window_to_foreground에서 오류 발생: {e}")
        return False
