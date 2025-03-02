import os
from PyPDF2 import PdfReader, PdfWriter

# 폴더 경로 설정
folder_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/1키움/WBM_cover"  # PDF 파일들이 있는 폴더
output_folder = os.path.join(folder_path, "output")  # 결과 PDF를 저장할 폴더

# 결과 폴더 생성
os.makedirs(output_folder, exist_ok=True)

print("=== PDF 첫 페이지 제거 작업 시작 ===")

# 폴더 내 모든 PDF 파일 처리
for file_name in os.listdir(folder_path):
    if file_name.lower().endswith(".pdf"):
        input_path = os.path.join(folder_path, file_name)
        output_path = os.path.join(output_folder, file_name)
        
        try:
            # PDF 읽기
            reader = PdfReader(input_path)
            writer = PdfWriter()

            # 첫 페이지를 제외한 나머지 페이지 추가
            for page_num in range(1, len(reader.pages)):  # 0번 인덱스(첫 페이지)를 제외
                writer.add_page(reader.pages[page_num])

            # 새로운 PDF 저장
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)

            print(f"처리 완료: {file_name} → {output_path}")

        except Exception as e:
            print(f"오류 발생: {file_name} - {e}")

print("=== 모든 PDF 첫 페이지 제거 작업 완료 ===")
