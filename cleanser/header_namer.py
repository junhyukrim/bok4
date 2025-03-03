import os
import re  # 정규표현식 모듈

def transform_txt_files(input_folder, output_folder):
    """
    txt 파일을 열고 첫 20글자를 파일명 앞에 붙여 새로운 폴더에 저장
    :param input_folder: 원본 txt 파일들이 있는 폴더 경로
    :param output_folder: 변환된 txt 파일을 저장할 폴더 경로
    """
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 입력 폴더 내 모든 txt 파일 순회
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # .txt 파일만 처리
            input_file_path = os.path.join(input_folder, filename)
            
            # 파일 열기
            with open(input_file_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            # 첫 20글자 추출
            first_20_chars = content[:20].replace("\n", " ").strip()  # 줄바꿈 제거 및 공백 정리
            
            # 숫자, 빈칸, 특수기호 제거 (정규표현식 사용)
            sanitized_chars = re.sub(r"[^가-힣a-zA-Z]", "", first_20_chars)  # 한글, 영어만 남김
            
            # 새로운 파일명 생성 (첫 20글자 + 기존 파일명)
            new_filename = f"{sanitized_chars}_{filename}"
            output_file_path = os.path.join(output_folder, new_filename)
            
            # 새 파일에 내용 저장
            with open(output_file_path, "w", encoding="utf-8") as new_file:
                new_file.write(content)
            
            print(f"Transformed: {filename} -> {new_filename}")

# 설정 값
input_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/현대차증권"  # 기존 txt 파일이 있는 폴더 경로
output_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/txt_out"  # 변환된 txt 파일을 저장할 폴더 경로

# 실행
transform_txt_files(input_folder, output_folder)
