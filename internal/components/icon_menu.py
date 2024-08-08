# File: icon_menu.py
# Path: internal\components\icon_menu.py

import os
from internal.icon_menu import icon_menu
from utils.my_logger import setup_logger

logger = setup_logger("IconMenu")

# 현재 스크립트의 디렉토리 경로를 가져옵니다.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 프로젝트의 루트 디렉토리 경로를 계산합니다. (components 폴더의 두 단계 위)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))

class IconMenu:
    @classmethod
    def new_profile(cls, hwnd):
        return icon_menu(hwnd, [
            os.path.join(PROJECT_ROOT, "resources", "img", "new_profile.png"),
            os.path.join(PROJECT_ROOT, "resources", "img", "new_profile_hover.png")
        ])

    @classmethod
    def quick(cls, hwnd):
        return icon_menu(hwnd, [
            os.path.join(PROJECT_ROOT, "resources", "img", "quick.png"),
            os.path.join(PROJECT_ROOT, "resources", "img", "quick_hover.png")
        ])

    @classmethod
    def profiles(cls, hwnd):
        return icon_menu(hwnd, [
            os.path.join(PROJECT_ROOT, "resources", "img", "profiles.png"),
            os.path.join(PROJECT_ROOT, "resources", "img", "profiles_hover.png")
        ])

    @classmethod
    def automation(cls, hwnd):
        return icon_menu(hwnd, [
            os.path.join(PROJECT_ROOT, "resources", "img", "automation.png"),
            os.path.join(PROJECT_ROOT, "resources", "img", "automation_hover.png")
        ])

    @classmethod
    def syncronizer(cls, hwnd):
        return icon_menu(hwnd, [
            os.path.join(PROJECT_ROOT, "resources", "img", "sync.png"),
            os.path.join(PROJECT_ROOT, "resources", "img", "sync_hover.png")
        ])

    @classmethod
    def team_members(cls, hwnd):
        return icon_menu(hwnd, [
            os.path.join(PROJECT_ROOT, "resources", "img", "team.png"),
            os.path.join(PROJECT_ROOT, "resources", "img", "team_hover.png")
        ])

    @classmethod
    def proxy_manager(cls, hwnd):
        return icon_menu(hwnd, [
            os.path.join(PROJECT_ROOT, "resources", "img", "proxy.png"),
            os.path.join(PROJECT_ROOT, "resources", "img", "proxy_hover.png")
        ])

    @classmethod
    def billing(cls, hwnd):
        return icon_menu(hwnd, [
            os.path.join(PROJECT_ROOT, "resources", "img", "billing.png"),
            os.path.join(PROJECT_ROOT, "resources", "img", "billing_hover.png")
        ])
