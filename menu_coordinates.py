# 프로그램 창의 좌표 (예시)
window_top_left = (277, 136)
window_bottom_right = (1643, 904)

# 창의 너비와 높이를 계산
window_width = window_bottom_right[0] - window_top_left[0]
window_height = window_bottom_right[1] - window_top_left[1]

# 버튼의 절대 좌표 (예시)
button_coordinates = {
    "New Profile": (324, 300),
    "Quick": (322, 355),
    "Profiles": (321, 394),
    "Automation": (327, 442),
    "Syncronizer": (323, 495),
    "Team Members": (318, 546),
    "Proxy Manager": (319, 600),
    "Billing": (316, 648)
}

# 상대 좌표 계산 및 상수로 정의
RELATIVE_COORDINATES = {
    name: ((abs_x - window_top_left[0]) / window_width, (abs_y - window_top_left[1]) / window_height)
    for name, (abs_x, abs_y) in button_coordinates.items()
}

def get_relative_coordinates(button_name):
    """
    주어진 버튼 이름에 대한 상대 좌표를 반환합니다.

    :param button_name: 버튼의 이름 (예: "New Profile")
    :return: 버튼의 상대 좌표 (x, y) 튜플. 버튼이 존재하지 않으면 None 반환.
    """
    return RELATIVE_COORDINATES.get(button_name)

# 예제 사용
button_name = "New Profile"
relative_position = get_relative_coordinates(button_name)

if relative_position:
    rel_x, rel_y = relative_position
    print(f"{button_name}: Relative Position (x: {rel_x:.4f}, y: {rel_y:.4f})")
else:
    print(f"Button '{button_name}' not found.")
