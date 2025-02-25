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

def rename_txt_file_based_on_pdf(pdf_path, txt_path):
    """
    PDF 파일의 제목을 기반으로 텍스트 파일 이름 변경.
    
    Args:
        pdf_path (str): PDF 파일의 경로.
        txt_path (str): 텍스트 파일의 경로.
    """
    # PDF 파일명 추출 (확장자 제거)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # 새로운 텍스트 파일 이름 생성
    new_name = f"{pdf_name}.txt"
    new_path = os.path.join(os.path.dirname(txt_path), new_name)
    
    # 텍스트 파일 이름 변경
    try:
        os.rename(txt_path, new_path)
        print(f"파일 이름이 '{txt_path}'에서 '{new_name}'으로 변경되었습니다.")
    except Exception as e:
        print(f"파일 이름 변경 중 오류 발생: {e}")

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
            rename_txt_file_based_on_pdf(pdf_path, txt_path)  # TXT 파일 이름 변경

# 경로 설정
pdf_folder_path = './pdf_files'  # PDF 파일이 담긴 폴더 경로
txt_folder_path = './txt_files'  # 변환된 TXT 파일을 저장할 폴더 경로

# 실행
process_pdf_folder(pdf_folder_path, txt_folder_path)
