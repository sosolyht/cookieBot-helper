# components/main_menu.py
from menu_finder import click_button


class ClickButton:
    @classmethod
    def new_profile(cls, hwnd):
        click_button(hwnd, ["img/new_profile.png", "img/new_profile_hover.png"])

    @classmethod
    def quick(cls, hwnd):
        click_button(hwnd, ["img/quick.png", "img/quick_hover.png"])

    @classmethod
    def profiles(cls, hwnd):
        click_button(hwnd, ["img/profiles.png", "img/profiles_hover.png"])

    @classmethod
    def automation(cls, hwnd):
        click_button(hwnd, ["img/automation.png", "img/automation_hover.png"])

    @classmethod
    def syncronizer(cls, hwnd):
        click_button(hwnd, ["img/sync.png", "img/sync_hover.png"])

    @classmethod
    def team_members(cls, hwnd):
        click_button(hwnd, ["img/team.png", "img/team_hover.png"])

    @classmethod
    def proxy_manager(cls, hwnd):
        click_button(hwnd, ["img/proxy.png", "img/proxy_hover.png"])

    @classmethod
    def billing(cls, hwnd):
        click_button(hwnd, ["img/billing.png", "img/billing_hover.png"])
