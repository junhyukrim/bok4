import os
import re

def clean_text_file(file_path):
    """
    텍스트 파일을 클렌징하여 원본에 직접 반영
    1. 괄호 () [] {} 및 괄호 안의 내용 제거
    2. '강세 요인 약세 요인' 이후의 모든 텍스트 제거
    :param file_path: 텍스트 파일 경로
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # 1. 괄호 및 괄호 안의 내용 제거
    content = re.sub(r"\(.*?\)|\[.*?\]|\{.*?\}", "", content)

    # 2. '강세 요인 약세 요인' 이후의 모든 텍스트 제거
    split_keyword = "강세 요인 약세 요인"
    if split_keyword in content:
        content = content.split(split_keyword)[0]

    # 원본 파일에 덮어쓰기
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Cleaned: {file_path}")

def process_folder(folder_path):
    """
    폴더 내 모든 텍스트 파일을 클렌징하여 원본에 직접 반영
    :param folder_path: 텍스트 파일들이 있는 폴더 경로
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # .txt 파일만 처리
            file_path = os.path.join(folder_path, filename)
            clean_text_file(file_path)

# 설정 값
folder_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/IBK/파란띠/long/cleansed"  # 텍스트 파일 폴더 경로

# 실행
process_folder(folder_path)
