from new_profile_menu_select import click_menu_item

class ProfileMenu:
    @classmethod
    def overview(cls, hwnd):
        print(f"Calling overview with hwnd: {hwnd}")
        return click_menu_item(hwnd, "Overview")

    @classmethod
    def proxy(cls, hwnd):
        print(f"Calling proxy with hwnd: {hwnd}")
        return click_menu_item(hwnd, "Proxy")

    @classmethod
    def extensions(cls, hwnd):
        print(f"Calling extensions with hwnd: {hwnd}")
        return click_menu_item(hwnd, "Extensions")

    @classmethod
    def timezone(cls, hwnd):
        print(f"Calling timezone with hwnd: {hwnd}")
        return click_menu_item(hwnd, "Timezone")

    @classmethod
    def webrtc(cls, hwnd):
        print(f"Calling webrtc with hwnd: {hwnd}")
        return click_menu_item(hwnd, "WebRTC")

    @classmethod
    def geolocation(cls, hwnd):
        print(f"Calling geolocation with hwnd: {hwnd}")
        return click_menu_item(hwnd, "Geolocation")

    @classmethod
    def advanced(cls, hwnd):
        print(f"Calling advanced with hwnd: {hwnd}")
        return click_menu_item(hwnd, "Advanced")

    @classmethod
    def cookies(cls, hwnd):
        print(f"Calling cookies with hwnd: {hwnd}")
        return click_menu_item(hwnd, "Cookies")

    @classmethod
    def bookmarks(cls, hwnd):
        print(f"Calling bookmarks with hwnd: {hwnd}")
        return click_menu_item(hwnd, "Bookmarks")
