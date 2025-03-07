import os
import re

def remove_page_numbers_from_file(input_file, output_file):
    """
    특정 페이지 번호 형식 (예: - 2 -)을 제거한 텍스트 파일을 저장합니다.

    :param input_file: 원본 텍스트 파일 경로
    :param output_file: 수정된 텍스트 파일 저장 경로
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 페이지 번호 패턴 제거 (예: "- 2 -", "- 10 -")
    cleaned_content = re.sub(r'^\s*-\s*\d+\s*-\s*$', '', content, flags=re.MULTILINE)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

def process_folder(input_folder, output_folder):
    """
    폴더 내 모든 .txt 파일에서 페이지 번호를 제거하고 결과를 출력 폴더에 저장합니다.

    :param input_folder: 입력 폴더 경로
    :param output_folder: 출력 폴더 경로
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            remove_page_numbers_from_file(input_path, output_path)

# 사용 예시
if __name__ == "__main__":
    input_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/original"  # 원본 텍스트 파일이 있는 폴더 경로
    output_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/page_removed"  # 수정된 텍스트 파일을 저장할 폴더 경로

    process_folder(input_folder, output_folder)

