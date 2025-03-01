import os
import re

def process_text(text):
    """
    텍스트에서 (cid:숫자) 형식을 처리:
    1. 문서 시작의 '(cid:숫자)' 형식은 삭제.
    2. 이후 나오는 '(cid:숫자)' 형식은 '.'으로 변환.
    3. 문서 마지막에 '.' 추가.
    """
    # 정규식 패턴 정의
    cid_pattern = r"\(cid:\d+\)"

    # 문서 시작의 '(cid:숫자)' 형식을 삭제
    if text.startswith('(cid:'):
        text = re.sub(cid_pattern, '', text, count=1).strip()

    # 이후 나오는 '(cid:숫자)' 형식을 '.'으로 변환
    text = re.sub(cid_pattern, '.', text)

    # 마지막에 '.' 추가 (이미 있으면 추가하지 않음)
    if not text.endswith('.'):
        text += '.'

    return text

def process_files_in_folder(folder_path):
    """
    폴더 내 모든 텍스트 파일을 처리하여 변환된 내용을 저장.
    
    :param folder_path: 텍스트 파일이 있는 폴더 경로
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 텍스트 파일만 처리
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 텍스트 변환 수행
            processed_content = process_text(content)

            # 변환된 내용을 동일한 파일에 덮어쓰기
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(processed_content)
            print(f"Processed: {filename}")

# 실행할 폴더 경로 설정
folder_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/1이트레이드/FCM/txted"  # 텍스트 파일이 있는 폴더 경로
process_files_in_folder(folder_path)
