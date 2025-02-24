import pdfplumber
import re
import os

def pdf_to_txt_with_pdfplumber(pdf_path, txt_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # per page
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# path
pdf_path = "제26차 금통위 의사록.pdf"
txt_path = "bok_minute_pdfplumber.txt"

# exe
pdf_to_txt_with_pdfplumber(pdf_path, txt_path)



def rename_txt_file_based_on_date(txt_path):
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
        print("날짜를 찾을 수 없습니다. 파일 이름 변경 실패.")

# 기존 텍스트 파일 경로
txt_path = "bok_minute_pdfplumber.txt"

# 함수 실행
rename_txt_file_based_on_date(txt_path)