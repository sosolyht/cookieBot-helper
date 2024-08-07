# File: main.py
# Path: main.py

import os

def add_file_path_comment(file_path, project_root):
    # 파일 경로와 파일명 가져오기 (프로젝트 루트 기준 상대 경로)
    relative_path = os.path.relpath(file_path, project_root)
    file_name = os.path.basename(file_path)

    print(f"Processing file: {relative_path}")  # 디버깅 출력

    # 파일 읽기
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.readlines()
    except Exception as e:
        print(f"Error reading file {relative_path}: {e}")
        return

    # 기존 주석 제거 및 import 문 찾기
    new_content = []
    import_found = False

    for line in content:
        if line.strip().startswith('import') or line.strip().startswith('from'):
            import_found = True
        if import_found:
            new_content.append(line)

    # 주석 생성
    comment = f"# File: {file_name}\n# Path: {relative_path}\n"

    # 파일 맨 위에 주석 추가하고, 주석과 import 사이에 빈 줄 하나 추가
    try:
        with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(comment + '\n' + ''.join(new_content))
        print(f"Added comment to file: {relative_path}")
    except Exception as e:
        print(f"Error writing file {relative_path}: {e}")

def main():
    # 프로젝트 루트 디렉토리 설정
    project_root = os.path.dirname(os.path.abspath(__file__))
    venv_dirs = ['venv', 'env', '.venv', '.env']  # 일반적인 가상 환경 디렉토리 이름

    # 모든 파이썬 파일을 탐색
    for root, _, files in os.walk(project_root):
        # 가상 환경 디렉토리를 무시
        if any(venv_dir in root for venv_dir in venv_dirs):
            continue

        for file in files:
            if file.endswith('.py'):  # .py 파일만 처리
                file_path = os.path.join(root, file)
                add_file_path_comment(file_path, project_root)


if __name__ == '__main__':
    main()
