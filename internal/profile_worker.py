# File: profile_worker.py
# Path: internal\profile_worker.py

import json
import time
from typing import Dict, Any, Optional
from utils.get_hwnd import get_hwnd
from utils.foreground import bring_window_to_foreground
from utils.my_logger import setup_logger
from internal.components.icon_menu import IconMenu
from internal.components.profile_menu import ProfileMenu
from internal.profile_menu import get_menu_coordinates, click_menu_item

logger = setup_logger(__name__)

class BrowserProfile:
    def __init__(self, profile: str, **data: Any):
        self.profile: str = profile
        self.data: Dict[str, Any] = data

def process_profile(json_data: str) -> Optional[BrowserProfile]:
    try:
        data = json.loads(json_data)
        profile = BrowserProfile(**data)
        logger.info("프로필이 성공적으로 생성되었습니다.")
        return profile
    except json.JSONDecodeError as e:
        logger.error(f"잘못된 JSON 형식입니다: {str(e)}")
    except Exception as e:
        logger.error(f"프로필 생성 중 오류 발생: {str(e)}")
    return None

def process_icon_menu():
    logger.info("아이콘 메뉴 처리 시작")
    time.sleep(1)  # 윈도우가 완전히 로드될 때까지 5초 대기

    hwnd = get_hwnd()
    if not hwnd or not bring_window_to_foreground(hwnd):
        logger.error("윈도우를 찾을 수 없거나 포그라운드로 가져올 수 없습니다")
        return False

    retry_count = 3
    for i in range(retry_count):
        if IconMenu.new_profile(hwnd):
            logger.info("New Profile 아이콘 선택 완료")
            return True
        else:
            logger.warning(f"New Profile 아이콘 선택 실패 (시도 {i+1}/{retry_count})")
            time.sleep(2)  # 재시도 전 2초 대기

    logger.error("New Profile 아이콘 선택 최종 실패")
    return False



def apply_profile_settings(profile: BrowserProfile):
    hwnd = get_hwnd()
    if not hwnd:
        logger.error("윈도우를 찾을 수 없습니다")
        return

    # 초기 메뉴 좌표 가져오기
    get_menu_coordinates(hwnd)

    for section, settings in profile.data.items():
        if section == "profile":
            continue  # profile은 이미 처리됨

        # 메뉴 항목 클릭 시도
        if click_menu_item(hwnd, section):
            logger.info(f"{section} 섹션 선택 완료")

            # 각 섹션별 설정 로직
            if section == "overview":
                logger.info(f"OS: {settings.get('os')}, Browser: {settings.get('browser')}")
            elif section == "proxy":
                logger.info(f"Proxy 설정: {settings.get('protocol')} - {settings.get('proxy')}")
            elif section == "extensions":
                logger.info("Extensions 설정")
            elif section == "timezone":
                logger.info("Timezone 설정")
            elif section == "webrtc":
                logger.info("WebRTC 설정")
            elif section == "geolocation":
                logger.info("Geolocation 설정")
            elif section == "advanced":
                logger.info(f"Start URL: {settings.get('start_url')}")
                logger.info(f"Screen Resolution: {settings.get('screen_resolution')}")
                logger.info(f"CPU: {settings.get('cpu')}, Memory: {settings.get('memory')} MB")
            elif section == "cookies":
                logger.info(f"{len(settings)} 개의 쿠키 설정")
            elif section == "bookmarks":
                bookmarks = settings.split(',')
                logger.info(f"{len(bookmarks)} 개의 북마크 설정")

            time.sleep(1)  # 설정 적용을 위한 대기 시간
        else:
            logger.error(f"{section} 섹션 선택 실패")
            # 메뉴 좌표 다시 가져오기 시도
            get_menu_coordinates(hwnd)


def execute_process():
    logger.info("프로세스 실행 시작")
    # 실행 단계 로직 추가
    logger.info("프로세스 실행 완료")

if __name__ == "__main__":
    # JSON 데이터 예제
    sample_message = '''
    {
        "profile": "Sample Profile",
        "overview": {
            "os": "Windows 10",
            "browser": "Chrome"
        },
        "proxy": {
            "protocol": "HTTP",
            "proxy": "192.168.1.1:8080"
        },
        "extensions": {},
        "timezone": {},
        "webrtc": {},
        "geolocation": {},
        "advanced": {
            "start_url": "https://www.example.com",
            "screen_resolution": "1920x1080",
            "cpu": 4,
            "memory": 8192
        },
        "cookies": [
            {
                "domain": ".example.com",
                "expirationdate": 1672531199,
                "hostonly": false,
                "httponly": false,
                "name": "session_id",
                "path": "/",
                "secure": true,
                "session": false,
                "value": "abc123"
            }
        ],
        "bookmarks": "https://www.example.com/bookmark1,https://www.example.com/bookmark2"
    }
    '''

    # Icon Menu 처리
    icon_menu_result = process_icon_menu()
    if not icon_menu_result:
        logger.warning("New Profile 아이콘을 찾지 못했습니다. 계속 진행합니다.")

    time.sleep(1)  # 아이콘 선택 후 10초 대기

    # 프로필 처리
    profile = process_profile(sample_message)
    if profile:
        logger.info(f"프로필 이름: {profile.profile}")
        apply_profile_settings(profile)

    time.sleep(0.5)  # 프로필 설정 적용 후 5초 대기

    # 실행 단계
    execute_process()

    logger.info("프로그램이 완료되었습니다.")
