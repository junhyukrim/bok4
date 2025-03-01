import os
import shutil
import pdfplumber

# 키워드 리스트 정의
keywords = ["<그림", "<표", "<도표"]  # 원하는 키워드를 여기에 추가

# 폴더 경로 설정
base_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/1_현대차증권/ficorange-graphtype"
keyword_yes_folder = os.path.join(base_folder, "keyword_yes")
keyword_none_folder = os.path.join(base_folder, "keyword_none")

# 결과 폴더 생성
os.makedirs(keyword_yes_folder, exist_ok=True)
os.makedirs(keyword_none_folder, exist_ok=True)

# PDF 파일 순회
for file_name in os.listdir(base_folder):
    if file_name.lower().endswith(".pdf"):
        pdf_path = os.path.join(base_folder, file_name)
        
        try:
            # PDF 첫 페이지 텍스트 추출
            with pdfplumber.open(pdf_path) as pdf:
                first_page_text = pdf.pages[0].extract_text()
            
            # 키워드 확인
            if any(keyword in first_page_text for keyword in keywords):
                shutil.move(pdf_path, os.path.join(keyword_yes_folder, file_name))
            else:
                shutil.move(pdf_path, os.path.join(keyword_none_folder, file_name))
        
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
