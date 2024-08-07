import boto3
from PIL import Image
from utils.aws_config import load_aws_config
from utils.my_logger import setup_logger

# 로거 설정
logger = setup_logger(__name__)


def aws_textract_helper(image_file_path, keywords=None):
    config = load_aws_config()

    # 이미지의 원래 크기 얻기
    with Image.open(image_file_path) as img:
        image_width, image_height = img.size

    logger.info(f"이미지 크기: {image_width}x{image_height}")

    textract = boto3.client(
        'textract',
        region_name=config['AWS']['Region'],
        aws_access_key_id=config['AWS']['AccessKeyID'],
        aws_secret_access_key=config['AWS']['SecretAccessKey']
    )

    logger.info("Textract 클라이언트 생성 완료")

    with open(image_file_path, 'rb') as document:
        image_bytes = document.read()

    logger.info("이미지 파일 읽기 완료")

    response = textract.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    logger.info("Textract로부터 응답 수신 완료")

    results = []

    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text = item['Text'].strip()  # 텍스트 전처리
            logger.info(f"텍스트 발견: {text}")

            if keywords is None or any(keyword == text for keyword in keywords):  # 정확한 문자열 매칭
                bounding_box = item['Geometry']['BoundingBox']
                left = bounding_box['Left'] * image_width
                top = bounding_box['Top'] * image_height
                width = bounding_box['Width'] * image_width
                height = bounding_box['Height'] * image_height

                logger.info(f"텍스트 '{text}' 위치: Left={left}, Top={top}, Width={width}, Height={height}")

                # 텍스트와 위치 정보를 튜플로 저장
                results.append((text, left, top, width, height))

    logger.info("텍스트 추출 및 위치 계산 완료")
    return results
