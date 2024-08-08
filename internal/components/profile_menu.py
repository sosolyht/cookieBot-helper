# File: profile_menu.py
# Path: internal\components\profile_menu.py

from internal.profile_menu import click_menu_item


class ProfileMenu:
    @classmethod
    def overview(cls, hwnd):
        return click_menu_item(hwnd, "Overview")

    @classmethod
    def proxy(cls, hwnd):
        return click_menu_item(hwnd, "Proxy")

    @classmethod
    def extensions(cls, hwnd):
        return click_menu_item(hwnd, "Extensions")

    @classmethod
    def timezone(cls, hwnd):
        return click_menu_item(hwnd, "Timezone")

    @classmethod
    def webrtc(cls, hwnd):
        return click_menu_item(hwnd, "WebRTC")

    @classmethod
    def geolocation(cls, hwnd):
        return click_menu_item(hwnd, "Geolocation")

    @classmethod
    def advanced(cls, hwnd):
        return click_menu_item(hwnd, "Advanced")

    @classmethod
    def cookies(cls, hwnd):
        return click_menu_item(hwnd, "Cookies")

    @classmethod
    def bookmarks(cls, hwnd):
        return click_menu_item(hwnd, "Bookmarks")

    @classmethod
    def execute_all(cls, hwnd):
        """
        모든 메뉴 항목을 순차적으로 클릭합니다.
        """
        cls.overview(hwnd)
        cls.proxy(hwnd)
        cls.extensions(hwnd)
        cls.timezone(hwnd)
        cls.webrtc(hwnd)
        cls.geolocation(hwnd)
        cls.advanced(hwnd)
        cls.cookies(hwnd)
        cls.bookmarks(hwnd)

# 사용 예시
# hwnd = get_hwnd()  # 특정 창의 핸들을 가져오는 함수
# ProfileMenu.execute_all(hwnd)

