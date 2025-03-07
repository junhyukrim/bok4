import pdfplumber 
import pytesseract
from pdf2image import convert_from_path
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# OCR을 위한 Tesseract 경로 설정 (Windows 사용 시 필요)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # 실제 설치 경로 입력

def pdf_to_txt(pdf_path, txt_path):
    """PDF를 텍스트로 변환 (OCR 포함)"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages if page.extract_text()])

        # OCR 적용: 텍스트가 없으면 OCR 실행
        if not text.strip():
            print(f" {pdf_path}는 이미지 PDF일 가능성이 높음 → OCR 실행")
            text = ocr_pdf(pdf_path)

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

    except Exception as e:
        print(f" PDF 변환 오류: {pdf_path} - {e}")

def ocr_pdf(pdf_path):
    """OCR을 사용하여 이미지 PDF에서 텍스트 추출"""
    try:
        images = convert_from_path(pdf_path)
        text = "\n".join([pytesseract.image_to_string(img, lang='kor+eng', config='--psm 3 --oem 1') for img in images])
        return text
    except Exception as e:
        print(f" OCR 변환 오류: {pdf_path} - {e}")
        return ""

def process_single_pdf(pdf_path, txt_folder_path):
    """PDF 하나를 변환하는 함수"""
    txt_file_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
    txt_path = os.path.join(txt_folder_path, txt_file_name)

    start_time = time.time()
    pdf_to_txt(pdf_path, txt_path)
    end_time = time.time()

    print(f"변환 완료: {txt_path} (소요 시간: {end_time - start_time:.2f}초)")

def filter_pdfs_by_date(pdf_folder_path, start_date, end_date):
    """지정된 날짜 범위 내의 PDF 파일만 필터링"""
    pdf_files = [os.path.join(pdf_folder_path, f) for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]

    # 파일명이 'YYMMDD_...' 형식이라고 가정하고 필터링
    filtered_files = []
    for pdf in pdf_files:
        try:
            file_name = os.path.basename(pdf)
            file_date_str = file_name[:6]  # 앞 6자리 추출 (YYMMDD)
            
            # 'YYMMDD'를 '20YYMMDD'로 변환
            file_date = datetime.strptime("20" + file_date_str, "%Y%m%d")

            if start_date <= file_date <= end_date:
                filtered_files.append(pdf)
        except ValueError:
            continue  # 날짜 형식이 맞지 않으면 건너뜀

    return filtered_files

def process_pdf_folder(pdf_folder_path, txt_folder_path, start_date, end_date, num_workers=8):
    """PDF 폴더 내에서 특정 기간의 파일을 병렬 처리"""
    os.makedirs(txt_folder_path, exist_ok=True)

    # 지정된 날짜 범위의 파일만 필터링
    pdf_files = filter_pdfs_by_date(pdf_folder_path, start_date, end_date)

    if not pdf_files:
        print(f" {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')} 기간 내 변환할 PDF 파일이 없습니다!")
        return

    print(f"총 {len(pdf_files)}개의 PDF 변환을 시작합니다...")

    # 멀티쓰레딩 적용 (속도 최적화)
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        executor.map(lambda pdf: process_single_pdf(pdf, txt_folder_path), pdf_files)

    print(f" 변환 완료! (저장 폴더: {txt_folder_path})")

# **경로 설정**
pdf_folder_path = './naver_reports_pdf'  # PDF 파일이 저장된 폴더
txt_folder_path = './txt_files'  # 변환된 TXT 파일을 저장할 폴더

# **변환할 날짜 범위 설정 (담당자가 직접 수정)**
start_date = datetime(2023, 3, 1)  # 시작 날짜 (예: 2023년 7월 24일)
end_date = datetime(2024, 2, 29)   # 종료 날짜 (예: 2023년 7월 25일)

# 전체 실행 (기간 내 파일만 변환)
process_pdf_folder(pdf_folder_path, txt_folder_path, start_date, end_date, num_workers=8)

