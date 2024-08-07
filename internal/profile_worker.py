# File: profile_worker.py
# Path: internal\profile_worker.py

import json
import datetime
from typing import List, Dict, Any, Optional
from PIL import Image
import time
from utils.screen_utils import capture_window, preprocess_image, extract_text
from profile_ import MenuClicker
from icon_menu import MainMenu

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
        self.overview: Overview = Overview(data.get('overview', {}))
        self.proxy: Proxy = Proxy(data.get('proxy', {}))
        self.extensions: Dict[str, Any] = data.get('extensions', {})
        self.timezone: Dict[str, Any] = data.get('timezone', {})
        self.webrtc: Dict[str, Any] = data.get('webrtc', {})
        self.geolocation: Dict[str, Any] = data.get('geolocation', {})
        self.advanced: Advanced = Advanced(data.get('advanced', {}))
        self.cookies: List[Cookie] = [Cookie(cookie) for cookie in data.get('cookies', [])]
        self.bookmarks: str = data.get('bookmarks', '')

def process_profile(json_data: str) -> Optional[BrowserProfile]:
    try:
        data = json.loads(json_data)
        profile = BrowserProfile(**data)
        print("프로필이 성공적으로 생성되었습니다.")
        return profile
    except json.JSONDecodeError as e:
        print(f"잘못된 JSON 형식입니다: {str(e)}")
        print(f"문제가 발생한 위치: {e.pos}")
        print(f"문제가 있는 줄: {json_data[max(0, e.pos - 20):e.pos + 20]}")
    except Exception as e:
        print(f"프로필 생성 중 오류 발생: {str(e)}")
    return None

def get_overview_text_and_image(pid: int) -> tuple[List[str], Optional[Image.Image]]:
    hwnd = bring_process_to_foreground(pid)  # 이 함수는 적절히 정의되어야 합니다.
    if hwnd:
        main_menu = MainMenu(hwnd)  # MainMenu 객체를 초기화합니다.
        clicker = MenuClicker(main_menu)  # MenuClicker에 MainMenu를 전달합니다.

        # Overview로 이동 시도
        if not clicker.Overview():
            print("Overview 클릭에 실패했습니다. NewProfile부터 다시 시도합니다.")
            # NewProfile 클릭 후 다시 Overview 시도
            if clicker.NewProfile():
                time.sleep(2)  # NewProfile이 로드될 때까지 대기
                if not clicker.Overview():
                    print("NewProfile 이후 Overview 클릭에 실패했습니다.")
                    return [], None
            else:
                print("NewProfile 클릭에 실패했습니다.")
                return [], None

        # Overview 클릭 성공 시
        time.sleep(2)  # Overview 페이지가 로드될 때까지 대기

        screenshot, offset = capture_window(hwnd, 0, 0, 0, 0)  # 전체 화면 캡처

        preprocessed_image = preprocess_image(screenshot)

        custom_config = r'--oem 3 --psm 6'
        data = extract_text(preprocessed_image, custom_config)

        all_text = []
        for i in range(len(data['level'])):
            if int(data['conf'][i]) > 60:
                text = data['text'][i].strip()
                if text:
                    all_text.append(text)

        return all_text, screenshot
    else:
        print("윈도우를 전경으로 가져오는 데 실패했습니다.")
        return [], None

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
        print(f"프로필 이름: {profile.profile}")
        print(f"OS: {profile.overview.os}")
        print(f"브라우저: {profile.overview.browser}")
        print(f"프록시 프로토콜: {profile.proxy.protocol}")
        print(f"프록시 주소: {profile.proxy.proxy}")
        print(f"시작 URL: {profile.advanced.start_url}")
        print(f"화면 해상도: {profile.advanced.screen_resolution}")
        print(f"CPU 코어 수: {profile.advanced.cpu}")
        print(f"메모리: {profile.advanced.memory}MB")

        if profile.cookies:
            print("쿠키:")
            for cookie in profile.cookies:
                print(f"  도메인: {cookie.domain}")
                print(f"  이름: {cookie.name}")
                print(f"  값: {cookie.value}")

        print(f"북마크: {profile.bookmarks}")

    # Overview 텍스트 및 이미지 가져오기
    pid = 16572  # 실제 프로세스 ID로 변경
    overview_text, screenshot = get_overview_text_and_image(pid)
    if overview_text:
        print("Overview 페이지의 텍스트:")
        for text in overview_text:
            print(text)

        if screenshot:
            # 이미지 저장
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"overview_screenshot_{timestamp}.png"
            screenshot.save(image_filename)
            print(f"스크린샷이 {image_filename}으로 저장되었습니다.")
    else:
        print("Overview 페이지의 텍스트와 이미지를 가져오는데 실패했습니다.")

print("프로그램이 완료되었습니다.")
