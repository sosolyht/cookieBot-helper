# File: test.py
# Path: test.py

import boto3
from PIL import Image
from utils.aws_config import load_aws_config

def extract_text_with_coordinates(image_file_path, config, keywords=None):
    # 이미지의 원래 크기 얻기
    with Image.open(image_file_path) as img:
        image_width, image_height = img.size

    textract = boto3.client(
        'textract',
        region_name=config['AWS']['Region'],
        aws_access_key_id=config['AWS']['AccessKeyID'],
        aws_secret_access_key=config['AWS']['SecretAccessKey']
    )

    with open(image_file_path, 'rb') as document:
        image_bytes = document.read()

    response = textract.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text = item['Text']
            if keywords:
                # 특정 키워드가 포함된 텍스트만 출력
                if any(keyword in text for keyword in keywords):
                    bounding_box = item['Geometry']['BoundingBox']
                    left = bounding_box['Left'] * image_width
                    top = bounding_box['Top'] * image_height
                    width = bounding_box['Width'] * image_width
                    height = bounding_box['Height'] * image_height

                    print(f"텍스트: {text}")
                    print(f"위치: Left={left}, Top={top}, Width={width}, Height={height}")
            else:
                bounding_box = item['Geometry']['BoundingBox']
                left = bounding_box['Left'] * image_width
                top = bounding_box['Top'] * image_height
                width = bounding_box['Width'] * image_width
                height = bounding_box['Height'] * image_height

                print(f"텍스트: {text}")
                print(f"위치: Left={left}, Top={top}, Width={width}, Height={height}")

# 설정 로드
config = load_aws_config()

# 이미지 파일 경로
image_file_path = 'Screenshot_2.png'

# 필터링할 키워드 리스트
keywords = ['Overview', 'Proxy', 'WebRTC']

# 텍스트 추출 및 필터링
extract_text_with_coordinates(image_file_path, config, keywords)
