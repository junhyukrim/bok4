import os
import pdfplumber

# 키워드 리스트 정의
keywords = ["Readers’ Cut", "Readers"]  # 원하는 키워드를 여기에 추가

# 폴더 경로 설정
base_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/한화"
keyword_yes_folder = os.path.join(base_folder, "readers_cut")

# 결과 폴더 생성
os.makedirs(keyword_yes_folder, exist_ok=True)

# bbox 설정 (예: 페이지의 특정 영역)
# (0, 0, 0, 0)으로 설정하면 페이지 전체에서 텍스트를 추출
bbox = (0, 100, 300, 180)  # x0, top, x1, bottom

# 페이지 설정 (1부터 시작)
page_number = 1  # 텍스트를 추출할 페이지 번호 (1부터 시작)

print("=== PDF 파일 분류 작업 시작 ===")

# PDF 파일 순회
for file_name in os.listdir(base_folder):
    if file_name.lower().endswith(".pdf"):
        pdf_path = os.path.join(base_folder, file_name)
        print(f"처리 중: {file_name}")

        try:
            # PDF 열기
            with pdfplumber.open(pdf_path) as pdf:
                # 지정된 페이지 번호가 유효한지 확인
                if page_number <= len(pdf.pages):
                    target_page = pdf.pages[page_number - 1]  # 페이지 번호는 0부터 시작하므로 -1 필요
                    
                    # bbox가 (0, 0, 0, 0)인 경우 전체 페이지에서 텍스트 추출
                    if bbox == (0, 0, 0, 0):
                        print(f"페이지 {page_number} 전체에서 텍스트 추출 중: {file_name}")
                        page_text = target_page.extract_text()
                    else:
                        # bbox가 지정된 경우 해당 영역에서 텍스트 추출
                        print(f"페이지 {page_number}, bbox({bbox}) 영역에서 텍스트 추출 중: {file_name}")
                        cropped_page = target_page.within_bbox(bbox)
                        page_text = cropped_page.extract_text() if cropped_page else ""
                else:
                    print(f"Error: {file_name}에는 페이지 {page_number}가 없습니다.")
                    continue

            # 키워드 확인
            if any(keyword in page_text for keyword in keywords):
                print(f"키워드 '{keywords}' 발견: {file_name} → 'last week' 폴더로 이동")
                new_path = os.path.join(keyword_yes_folder, file_name)
                os.rename(pdf_path, new_path)
            else:
                print(f"키워드 '{keywords}' 미발견: {file_name} → 현재 폴더에 유지")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

print("=== PDF 파일 분류 작업 완료 ===")
