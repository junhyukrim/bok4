import pdfplumber
import re
import os

def pdf_to_txt_with_pdfplumber(pdf_path, txt_path):
    """PDF 파일을 텍스트로 변환"""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # 페이지별 텍스트 추출
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def rename_txt_file_based_on_date(txt_path):
    """텍스트 파일 내용에서 날짜를 추출하여 파일 이름 변경"""
    with open(txt_path, 'r', encoding='utf-8') as file:
        content = file.read()
    match = re.search(r'(\d{4})년 (\d{1,2})월 (\d{1,2})일', content)
    if match:
        year, month, day = match.groups()
        date_str = f"{year}{int(month):02d}{int(day):02d}"
        new_name = f"{date_str}_bok_min.txt"
        new_path = os.path.join(os.path.dirname(txt_path), new_name)
        os.rename(txt_path, new_path)
        print(f"파일 이름이 '{txt_path}'에서 '{new_name}'으로 변경되었습니다.")
    else:
        print(f"날짜를 찾을 수 없습니다. 파일 이름 변경 실패: {txt_path}")

def process_pdf_folder(pdf_folder_path, txt_folder_path):
    """PDF 폴더 내 모든 파일을 처리하여 텍스트로 변환 후 저장"""
    # 텍스트 저장 폴더가 없으면 생성
    if not os.path.exists(txt_folder_path):
        os.makedirs(txt_folder_path)

    # PDF 폴더 내 모든 PDF 파일 처리
    for file_name in os.listdir(pdf_folder_path):
        if file_name.endswith('.pdf'):  # PDF 파일만 처리
            pdf_path = os.path.join(pdf_folder_path, file_name)
            txt_file_name = os.path.splitext(file_name)[0] + ".txt"
            txt_path = os.path.join(txt_folder_path, txt_file_name)

            print(f"Processing PDF: {file_name}")
            pdf_to_txt_with_pdfplumber(pdf_path, txt_path)  # PDF → TXT 변환

            print(f"Renaming TXT: {txt_file_name}")
            rename_txt_file_based_on_date(txt_path)  # TXT 파일 이름 변경

# 경로 설정
pdf_folder_path = './pdf_files'  # PDF 파일이 담긴 폴더 경로
txt_folder_path = './txt_files'  # 변환된 TXT 파일을 저장할 폴더 경로

# 실행
process_pdf_folder(pdf_folder_path, txt_folder_path)
