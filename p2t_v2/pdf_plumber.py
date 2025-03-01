import pdfplumber

def extract_text_from_pages(pdf_path, page_numbers, bbox):
    """
    PDF의 여러 페이지에서 지정된 영역(bbox)의 텍스트를 추출
    :param pdf_path: PDF 파일 경로
    :param page_numbers: 추출할 페이지 번호 리스트 (0부터 시작)
    :param bbox: 본문 영역 좌표 (x0, y0, x1, y1)
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
            
            # 지정된 bbox 영역 내의 텍스트 추출
            cropped_page = page.within_bbox(bbox)
            text = cropped_page.extract_text() if cropped_page else None
            
            # 결과 저장
            extracted_texts[page_number] = text
    
    return extracted_texts

# PDF 파일 경로
pdf_path = "이트레이드증권_140416_1.pdf"

# 추출할 페이지 번호 리스트 (예: 1페이지와 2페이지)
page_numbers = [0]

# 본문 영역 좌표 설정 (x0, y0, x1, y1)
bbox = (10, 150, 550, 800)  # 좌표는 PDF 레이아웃에 따라 조정 필요

# 여러 페이지에서 본문 텍스트 추출
texts_by_page = extract_text_from_pages(pdf_path, page_numbers=page_numbers, bbox=bbox)

# 결과 출력
for page_num, text in texts_by_page.items():
    print(f"=== 페이지 {page_num + 1} ===")
    print(text)

