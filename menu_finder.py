import psutil
import win32gui
import win32com.client
import win32process
from PIL import Image
import time
import cv2
import numpy as np
import mss
import pyautogui
import ctypes

button_images = {
    "New Profile": ["img/new_profile.png", "img/new_profile_hover.png"],
    "Quick": ["img/quick.png", "img/quick_hover.png"],
    "Profiles": ["img/profiles.png", "img/profiles_hover.png"],
    "Automation": ["img/automation.png", "img/automation_hover.png"],
    "Syncronizer": ["img/sync.png", "img/sync_hover.png"],
    "Team Members": ["img/team.png", "img/team_hover.png"],
    "Proxy Manager": ["img/proxy.png", "img/proxy_hover.png"],
    "Billing": ["img/billing.png", "img/billing_hover.png"]
}


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


def capture_client_area(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    left, top, right, bottom = rect
    client_left, client_top, client_right, client_bottom = client_rect

    border_left = (right - left - client_right) // 2
    title_bar = bottom - top - client_bottom - border_left

    with mss.mss() as sct:
        monitor = {
            "top": top + title_bar,
            "left": left + border_left,
            "width": client_right,
            "height": client_bottom
        }
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
        img.save("client_area_screenshot.png")
        print(f"Client area screenshot saved as client_area_screenshot.png")

        return np.array(img)


def find_button_advanced(screenshot, button_name):
    button_images_list = button_images[button_name]
    best_match = None
    best_value = -1
    best_size = None

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("debug_screenshot.png", screenshot)
    for idx, img_path in enumerate(button_images_list):
        template = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"Failed to load image: {img_path}")
            continue

        cv2.imwrite(f"debug_template_{button_name}_{idx}.png", template)

        h, w = template.shape[:2]

        # 전체 이미지 매칭
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        print(f"Button: {button_name}, Image: {img_path}, Max value: {max_val}")

        if max_val > best_value:
            best_value = max_val
            best_match = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            best_size = (w, h)

    if best_value > 0.7:  # 임계값 조정
        print(f"Best match for {button_name}: value={best_value}, location={best_match}")
        return best_match, best_size
    else:
        print(f"No good match found for {button_name}. Best value: {best_value}")
        return None, None


def click_button(hwnd, button_name):
    # 화면 업데이트를 위해 충분히 기다립니다
    time.sleep(2)

    screenshot = capture_client_area(hwnd)
    location, size = find_button_advanced(screenshot, button_name)  # find_button_advanced 사용

    if location is not None:
        rect = win32gui.GetWindowRect(hwnd)
        client_rect = win32gui.GetClientRect(hwnd)
        left, top, right, bottom = rect
        client_left, client_top, client_right, client_bottom = client_rect

        border_left = (right - left - client_right) // 2
        title_bar = bottom - top - client_bottom - border_left

        dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
        scale_factor = dpi / 96.0

        button_x, button_y = location
        click_x = left + border_left + int(button_x / scale_factor)
        click_y = top + title_bar + int(button_y / scale_factor)

        print(f"Window rect: {rect}")
        print(f"Client rect: {client_rect}")
        print(f"DPI: {dpi}, Scale factor: {scale_factor}")
        print(f"Button location: {location}")
        print(f"Button size: {size}")
        print(f"Clicking on {button_name} at ({click_x}, {click_y})")

        # 클릭 전 위치 재확인
        pyautogui.moveTo(click_x, click_y)
        time.sleep(0.5)
        screenshot = capture_client_area(hwnd)
        new_location, new_size = find_button_advanced(screenshot, button_name)  # find_button_advanced 사용
        if new_location:
            new_click_x = left + border_left + int(new_location[0] / scale_factor)
            new_click_y = top + title_bar + int(new_location[1] / scale_factor)
            print(f"Adjusted click position: ({new_click_x}, {new_click_y})")
            click_x, click_y = new_click_x, new_click_y

        pyautogui.click(click_x, click_y)
    else:
        print(f"Button '{button_name}' not found.")


if __name__ == "__main__":

    pid = 17736  # 원하는 PID로 변경하세요

    try:
        process = psutil.Process(pid)
        print(f"Found process: {process.name()} (PID: {pid})")

        hwnd = bring_process_to_foreground(pid)
        if hwnd:
            # 윈도우가 포그라운드로 올 때까지 충분히 기다립니다
            time.sleep(2)

            # 모든 버튼을 순서대로 클릭
            for button_name in button_images.keys():
                print(f"Attempting to click {button_name}")
                click_button(hwnd, button_name)
                time.sleep(2)  # 각 클릭 사이에 2초 대기

        else:
            print("Failed to bring the window to foreground.")
    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}")
    except Exception as e:
        print(f"An error occurred: {e}")

