# File: test.py
# Path: test.py

from utils.get_hwnd import get_hwnd
from internal.components.icon_menu import IconMenu

def main():
    # get_hwnd 함수를 사용하여 특정 창의 핸들을 가져옵니다.
    hwnd = get_hwnd()

    if hwnd:
        # IconMenu의 new_profile 메서드를 호출하여 버튼을 클릭합니다.
        IconMenu.new_profile(hwnd)
    else:
        print("Hidemyacc 3.0.69 창을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
