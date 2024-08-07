#new_profile_menu_select.py
import psutil
import win32gui
import win32con
import win32com.client
import win32process
import time
import pyautogui
from screen_utils import calculate_relative_coords, capture_window, preprocess_image, extract_text

class MenuClicker:
    def __init__(self):
        self.MENU_ITEMS = [
        "Overview", "Proxy", "Extensions", "Timezone", "WebRTC",
        "Geolocation", "Advanced", "Cookies", "Bookmarks"
        ]
        self.calculate_coords = calculate_relative_coords(1366, 768, 50/1366, 76/768, 300/1366, 614/768)

    def bring_process_to_foreground(self, pid):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)

        if hwnds:
            hwnd = hwnds[0]
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')  # Alt 키를 보내서 창을 활성화
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 최소화된 창을 복원
            win32gui.SetForegroundWindow(hwnd)
            win32gui.BringWindowToTop(hwnd)
            return hwnd
        else:
            print(f"No visible window found for PID {pid}")
            return None

    def extract_text_and_click(self, image, hwnd, offset, target_text):
        custom_config = r'--oem 3 --psm 6 -l eng -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        data = extract_text(image, custom_config)

        for i in range(len(data['level'])):
            if int(data['conf'][i]) > 0 and data['text'][i] == target_text:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                print(f"Found '{target_text}' at: ({x}, {y}, {w}, {h}) in image coordinates")

                click_x = x + w // 2
                click_y = y + h // 2

                rect = win32gui.GetWindowRect(hwnd)
                left, top, _, _ = rect
                actual_click_x = left + offset[0] + click_x
                actual_click_y = top + offset[1] + click_y

                print(f"Clicking at: ({actual_click_x}, {actual_click_y})")
                pyautogui.click(actual_click_x, actual_click_y)
                return True
        return False

    def click_menu_item(self, pid, menu_item):
        if menu_item not in self.MENU_ITEMS:
            print(f"Invalid menu item: {menu_item}")
            return False

        try:
            process = psutil.Process(pid)
            print(f"Found process: {process.name()} (PID: {pid})")

            hwnd = self.bring_process_to_foreground(pid)
            if hwnd:
                time.sleep(1)

                x, y, width, height = self.calculate_coords(hwnd)
                screenshot, offset = capture_window(hwnd, x, y, width, height)

                preprocessed_image = preprocess_image(screenshot)

                print(f"Extracting text and clicking on '{menu_item}' from the preprocessed screenshot...")
                if not self.extract_text_and_click(preprocessed_image, hwnd, offset, menu_item):
                    print(f"'{menu_item}' text not found in the image.")
                    return False
                return True
            else:
                print("Failed to bring the window to foreground.")
                return False
        except psutil.NoSuchProcess:
            print(f"No process found with PID {pid}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False


    def Overview(self, pid):
        return self.click_menu_item(pid, "Overview")

    def Proxy(self, pid):
        return self.click_menu_item(pid, "Proxy")

    def Extensions(self, pid):
        return self.click_menu_item(pid, "Extensions")

    def Timezone(self, pid):
        return self.click_menu_item(pid, "Timezone")

    def WebRTC(self, pid):
        return self.click_menu_item(pid, "WebRTC")

    def Geolocation(self, pid):
        return self.click_menu_item(pid, "Geolocation")

    def Advanced(self, pid):
        return self.click_menu_item(pid, "Advanced")

    def Cookies(self, pid):
        return self.click_menu_item(pid, "Cookies")

    def Bookmarks(self, pid):
        return self.click_menu_item(pid, "Bookmarks")

if __name__ == "__main__":
    pid = 17736  # 원하는 PID로 변경하세요

    clicker = MenuClicker()

    # Proxy 메뉴 클릭
    success = clicker.Proxy(pid)
    if success:
        print("Successfully clicked on Proxy")
    else:
        print("Failed to click on Proxy")

    # WebRTC 메뉴 클릭
    success = clicker.WebRTC(pid)
    if success:
        print("Successfully clicked on WebRTC")
    else:
        print("Failed to click on WebRTC")
