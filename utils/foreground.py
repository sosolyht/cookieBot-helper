import win32gui
import win32process
import psutil


def bring_window_to_foreground(hwnd):
    try:
        # 창 핸들이 유효한지 확인합니다.
        if not win32gui.IsWindow(hwnd):
            print("Invalid window handle.")
            return None

        # 윈도우 핸들로부터 프로세스 ID를 가져옵니다.
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        # 주어진 PID가 현재 실행 중인지 확인합니다.
        if not psutil.pid_exists(pid):
            print(f"Error: No process found with PID {pid}")
            return None

        print(f"Attempting to bring window with handle {hwnd} to foreground.")

        # 창을 포그라운드로 가져옵니다.
        try:
            win32gui.SetForegroundWindow(hwnd)
            print(f"Window with handle {hwnd} is now in the foreground.")
        except Exception as e:
            print(f"Failed to set foreground window: {e}")
            return None

        return hwnd

    except Exception as e:
        print(f"Error in bring_window_to_foreground: {e}")
        return None
