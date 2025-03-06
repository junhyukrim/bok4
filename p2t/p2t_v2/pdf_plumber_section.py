import pdfplumber

# PDF 파일 경로
pdf_path = "키움증권_221215_1.pdf"

# 키워드 설정
start_keyword = "Check Point"
section_start_pattern = "\\section*{"  # 다음 섹션의 시작 패턴

def extract_check_point(pdf_path, start_keyword, section_start_pattern):
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # 페이지에서 텍스트 추출
            text = page.extract_text()
            
            if text and start_keyword in text:
                print(f"'{start_keyword}' 발견 (페이지 {page_number})")
                
                # 키워드 이후의 텍스트 추출
                start_index = text.find(start_keyword)
                extracted_text = text[start_index:]
                
                # 다음 섹션 패턴을 기준으로 종료 지점 설정
                next_section_start = extracted_text.find(section_start_pattern)
                if next_section_start != -1:
                    extracted_text = extracted_text[:next_section_start]
                
                return extracted_text.strip()
    
    return None

# "Check Point" 섹션 내용 추출
check_point_text = extract_check_point(pdf_path, start_keyword, section_start_pattern)

if check_point_text:
    print("\n=== 'Check Point' 섹션 텍스트 ===\n")
    print(check_point_text)
else:
    print(f"'{start_keyword}' 섹션을 찾을 수 없습니다.")
