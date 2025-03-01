import pdfplumber

def extract_text_from_columns(pdf_path, page_numbers, bbox_column1, bbox_column2):
    """
    PDF의 여러 페이지에서 두 열로 나뉜 텍스트를 추출하고 결합
    :param pdf_path: PDF 파일 경로
    :param page_numbers: 추출할 페이지 번호 리스트 (0부터 시작)
    :param bbox_column1: 첫 번째 열의 본문 영역 좌표 (x0, y0, x1, y1)
    :param bbox_column2: 두 번째 열의 본문 영역 좌표 (x0, y0, x1, y1)
    :return: 페이지별로 추출된 텍스트 딕셔너리 (페이지 번호를 키로 사용)
    """
    extracted_texts = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_number in page_numbers:
            # 페이지 번호가 유효한지 확인
            if page_number < 0 or page_number >= len(pdf.pages):
                print(f"페이지 번호 {page_number}는 유효하지 않습니다.")
                continue
            
            # 특정 페이지 선택
            page = pdf.pages[page_number]
            
            # 첫 번째 열 텍스트 추출
            cropped_page_col1 = page.within_bbox(bbox_column1)
            text_col1 = cropped_page_col1.extract_text() if cropped_page_col1 else ""
            
            # 두 번째 열 텍스트 추출
            cropped_page_col2 = page.within_bbox(bbox_column2)
            text_col2 = cropped_page_col2.extract_text() if cropped_page_col2 else ""
            
            # 두 열의 텍스트를 순서대로 결합
            combined_text = f"{text_col1}\n{text_col2}"
            
            # 결과 저장
            extracted_texts[page_number] = combined_text
    
    return extracted_texts

# PDF 파일 경로
pdf_path = "이트레이드증권_150128_1.pdf"

# 추출할 페이지 번호 리스트 (예: 1페이지만)
page_numbers = [0]

# 첫 번째 열 본문 영역 좌표 설정 (x0, y0, x1, y1)
bbox_column1 = (10, 100, 280, 300)  # 좌표는 PDF 레이아웃에 따라 조정 필요

# 두 번째 열 본문 영역 좌표 설정 (x0, y0, x1, y1)
bbox_column2 = (280, 100, 580, 300)  # 좌표는 PDF 레이아웃에 따라 조정 필요

# 여러 페이지에서 두 열의 텍스트 추출 및 결합
texts_by_page = extract_text_from_columns(pdf_path, page_numbers=page_numbers,
                                          bbox_column1=bbox_column1,
                                          bbox_column2=bbox_column2)

# 결과 출력
for page_num, text in texts_by_page.items():
    print(f"=== 페이지 {page_num + 1} ===")
    print(text)
