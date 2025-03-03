import os
import pdfplumber

def extract_text_from_columns(pdf_path, page_number, bbox_column1, bbox_column2):
    """
    PDF의 특정 페이지에서 두 열로 나뉜 텍스트를 추출하고 결합
    :param pdf_path: PDF 파일 경로
    :param page_number: 추출할 페이지 번호 (0부터 시작)
    :param bbox_column1: 첫 번째 열의 본문 영역 좌표 (x0, y0, x1, y1)
    :param bbox_column2: 두 번째 열의 본문 영역 좌표 (x0, y0, x1, y1)
    :return: 결합된 텍스트
    """
    with pdfplumber.open(pdf_path) as pdf:
        if page_number < len(pdf.pages):  # 페이지 번호가 유효한지 확인
            page = pdf.pages[page_number]
            
            # 첫 번째 열 텍스트 추출
            cropped_page_col1 = page.within_bbox(bbox_column1)
            text_col1 = cropped_page_col1.extract_text() if cropped_page_col1 else ""
            
            # 두 번째 열 텍스트 추출
            cropped_page_col2 = page.within_bbox(bbox_column2)
            text_col2 = cropped_page_col2.extract_text() if cropped_page_col2 else ""
            
            # 두 열의 텍스트를 순서대로 결합
            return f"{text_col1}\n{text_col2}"
        else:
            print(f"Page {page_number} does not exist in {pdf_path}")
            return ""

def process_pdfs_in_folder(input_folder, output_folder, page_number, bbox_column1, bbox_column2):
    """
    폴더 내 모든 PDF 파일을 처리하여 지정된 페이지와 영역의 텍스트를 추출 후 저장 (2열 대응)
    :param input_folder: PDF 파일이 있는 폴더 경로
    :param output_folder: 추출된 텍스트를 저장할 폴더 경로
    :param page_number: 추출할 페이지 번호 (0부터 시작)
    :param bbox_column1: 첫 번째 열의 본문 영역 좌표 (x0, y0, x1, y1)
    :param bbox_column2: 두 번째 열의 본문 영역 좌표 (x0, y0, x1, y1)
    """
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 입력 폴더 내 모든 PDF 파일 순회
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):  # .pdf 파일만 처리
            pdf_path = os.path.join(input_folder, filename)
            
            # 텍스트 추출 (두 열 처리)
            extracted_text = extract_text_from_columns(pdf_path, page_number, bbox_column1, bbox_column2)
            
            # 결과 저장 (파일 이름은 .txt로 변경)
            output_file_name = os.path.splitext(filename)[0] + ".txt"
            output_file_path = os.path.join(output_folder, output_file_name)
            
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(extracted_text)
            
            print(f"Processed: {filename} -> {output_file_name}")

# 설정 값
input_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/1_현대차증권/ficorange-graphtype/keyword_yes"  # PDF 파일이 있는 폴더 경로
output_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/1_현대차증권/ficorange-graphtype/keyword_yes/txted"  # 추출된 텍스트 저장 폴더 경로
page_number = 0  # 첫 번째 페이지(0부터 시작)

# 첫 번째 열 본문 영역 좌표 설정 (x0, y0, x1, y1)
bbox_column1 = (150, 120, 550, 300)  # 좌표는 PDF 레이아웃에 따라 조정 필요

# 두 번째 열 본문 영역 좌표 설정 (x0, y0, x1, y1)
bbox_column2 = (20, 300, 550, 700)  # 좌표는 PDF 레이아웃에 따라 조정 필요

# 실행
process_pdfs_in_folder(input_folder, output_folder, page_number,
                       bbox_column1=bbox_column1,
                       bbox_column2=bbox_column2)
