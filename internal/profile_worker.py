# File: profile_worker.py
# Path: internal\profile_worker.py

import json
import datetime
from typing import List, Dict, Any, Optional
from PIL import Image
import time
from utils.screen_utils import capture_window, preprocess_image, extract_text, save_image
from internal.components.profile_menu import ProfileMenu
from utils.foreground import bring_window_to_foreground
from utils.my_logger import setup_logger
from utils.get_hwnd import get_hwnd

logger = setup_logger(__name__)

class Overview:
    def __init__(self, data: Dict[str, str]):
        self.os: str = data.get('os', '')
        self.browser: str = data.get('browser', '')

class Proxy:
    def __init__(self, data: Dict[str, str]):
        self.protocol: str = data.get('protocol', '')
        self.proxy: str = data.get('proxy', '')

class Advanced:
    def __init__(self, data: Dict[str, Any]):
        self.start_url: str = data.get('start_url', '')
        self.screen_resolution: str = data.get('screen_resolution', '')
        self.cpu: int = data.get('cpu', 0)
        self.memory: int = data.get('memory', 0)

class Cookie:
    def __init__(self, data: Dict[str, Any]):
        self.domain: str = data.get('domain', '')
        self.expirationdate: float = data.get('expirationdate', 0.0)
        self.hostonly: bool = data.get('hostonly', False)
        self.httponly: bool = data.get('httponly', False)
        self.name: str = data.get('name', '')
        self.path: str = data.get('path', '')
        self.samesite: Optional[str] = data.get('samesite')
        self.secure: bool = data.get('secure', False)
        self.session: bool = data.get('session', False)
        self.storeid: Optional[str] = data.get('storeid')
        self.value: str = data.get('value', '')

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

def process_profile_sections(profile: BrowserProfile):
    hwnd = get_hwnd()
    if not hwnd:
        logger.error("Hidemyacc 윈도우를 찾을 수 없습니다.")
        return

    if not bring_window_to_foreground(hwnd):
        logger.error("윈도우를 포그라운드로 가져오는 데 실패했습니다.")
        return

    for section in profile.data.keys():
        logger.info(f"Processing {section.capitalize()} section")
        section_method = getattr(ProfileMenu, section.lower(), None)
        if section_method is None:
            logger.warning(f"섹션 '{section}'에 해당하는 메서드를 찾을 수 없습니다. 다음 섹션으로 넘어갑니다.")
            continue

        try:
            if section_method(hwnd):
                logger.info(f"{section.capitalize()} 메뉴 클릭 성공")
                time.sleep(2)  # 페이지가 로드될 때까지 대기
                # 여기에 각 섹션에 대한 추가 처리를 할 수 있습니다.
            else:
                logger.warning(f"{section.capitalize()} 메뉴 클릭 실패")
        except Exception as e:
            logger.error(f"{section.capitalize()} 처리 중 오류 발생: {str(e)}")

        logger.info(f"{section.capitalize()} 섹션 처리 완료")

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

    # 프로필 처리
    profile = process_profile(sample_message)
    if profile:
        logger.info(f"프로필 이름: {profile.profile}")
        process_profile_sections(profile)

logger.info("프로그램이 완료되었습니다.")
