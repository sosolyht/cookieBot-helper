import psutil
import win32gui
import win32com.client
import win32process

def bring_process_to_foreground(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)

    if hwnds:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnds[0])
        win32gui.BringWindowToTop(hwnds[0])
        return hwnds[0]
    else:
        print(f"No visible window found for PID {pid}")
        return None

def get_window_coordinates(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    return left, top, right, bottom

def record_window_coordinates(pid):
    hwnd = bring_process_to_foreground(pid)
    if hwnd:
        left, top, right, bottom = get_window_coordinates(hwnd)
        with open("window_coordinates.txt", "w") as file:
            file.write(f"Top-left corner: ({left}, {top})\n")
            file.write(f"Bottom-right corner: ({right}, {bottom})\n")
        print(f"Window coordinates recorded: Top-left ({left}, {top}), Bottom-right ({right}, {bottom})")
    else:
        print("Failed to bring process to foreground.")

if __name__ == "__main__":
    pid = 17736  # 여기서 원하는 PID로 변경하세요

    try:
        process = psutil.Process(pid)
        print(f"Found process: {process.name()} (PID: {pid})")

        record_window_coordinates(pid)

    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}")
    except Exception as e:
        print(f"An error occurred: {e}")
