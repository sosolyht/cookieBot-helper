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
