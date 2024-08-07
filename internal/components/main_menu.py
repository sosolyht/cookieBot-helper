# File: main_menu.py
# Path: internal\components\main_menu.py

from internal.icon_menu import icon_menu


class IconMenu:
    @classmethod
    def new_profile(cls, hwnd):
        icon_menu(hwnd, ["resources/img/new_profile.png", "resources/img/new_profile_hover.png"])

    @classmethod
    def quick(cls, hwnd):
        icon_menu(hwnd, ["resources/img/quick.png", "resources/img/quick_hover.png"])

    @classmethod
    def profiles(cls, hwnd):
        icon_menu(hwnd, ["resources/img/profiles.png", "resources/img/profiles_hover.png"])

    @classmethod
    def automation(cls, hwnd):
        icon_menu(hwnd, ["resources/img/automation.png", "resources/img/automation_hover.png"])

    @classmethod
    def syncronizer(cls, hwnd):
        icon_menu(hwnd, ["resources/img/sync.png", "resources/img/sync_hover.png"])

    @classmethod
    def team_members(cls, hwnd):
        icon_menu(hwnd, ["resources/img/team.png", "resources/img/team_hover.png"])

    @classmethod
    def proxy_manager(cls, hwnd):
        icon_menu(hwnd, ["resources/img/proxy.png", "resources/img/proxy_hover.png"])

    @classmethod
    def billing(cls, hwnd):
        icon_menu(hwnd, ["resources/img/billing.png", "resources/img/billing_hover.png"])
