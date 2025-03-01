import os
import pdfplumber

def extract_text_from_page(pdf_path, page_number, bbox):
    """
    PDF의 특정 페이지에서 지정된 영역(bbox)의 텍스트를 추출
    :param pdf_path: PDF 파일 경로
    :param page_number: 추출할 페이지 번호 (0부터 시작)
    :param bbox: 본문 영역 좌표 (x0, y0, x1, y1)
    :return: 추출된 텍스트
    """
    with pdfplumber.open(pdf_path) as pdf:
        # 특정 페이지 선택
        if page_number < len(pdf.pages):  # 페이지 번호가 유효한지 확인
            page = pdf.pages[page_number]
            
            # 지정된 bbox 영역 내의 텍스트 추출
            cropped_page = page.within_bbox(bbox)
            text = cropped_page.extract_text() if cropped_page else ""
            return text
        else:
            print(f"Page {page_number} does not exist in {pdf_path}")
            return ""

def process_pdfs_in_folder(input_folder, output_folder, page_number, bbox):
    """
    폴더 내 모든 PDF 파일을 처리하여 지정된 페이지와 영역의 텍스트를 추출 후 저장
    :param input_folder: PDF 파일이 있는 폴더 경로
    :param output_folder: 추출된 텍스트를 저장할 폴더 경로
    :param page_number: 추출할 페이지 번호 (0부터 시작)
    :param bbox: 본문 영역 좌표 (x0, y0, x1, y1)
    """
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 입력 폴더 내 모든 PDF 파일 순회
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):  # .pdf 파일만 처리
            pdf_path = os.path.join(input_folder, filename)
            
            # 텍스트 추출
            extracted_text = extract_text_from_page(pdf_path, page_number, bbox)
            
            # 결과 저장 (파일 이름은 .txt로 변경)
            output_file_name = os.path.splitext(filename)[0] + ".txt"
            output_file_path = os.path.join(output_folder, output_file_name)
            
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(extracted_text)
            
            print(f"Processed: {filename} -> {output_file_name}")

# 설정 값
input_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/1_현대차증권/ficorange-nonetype"  # PDF 파일이 있는 폴더 경로
output_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/1_현대차증권/ficorange-nonetype/txted"  # 추출된 텍스트 저장 폴더 경로
page_number = 0  # 첫 번째 페이지(0부터 시작)
bbox = (150, 150, 550, 800)  # 본문 좌표 (x0, y0, x1, y1)

# 실행
process_pdfs_in_folder(input_folder, output_folder, page_number, bbox)
