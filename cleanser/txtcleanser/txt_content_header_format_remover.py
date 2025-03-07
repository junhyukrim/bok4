import os
import re

def process_file(input_file, output_file):
    """
    텍스트 파일에서 '( )' 또는 '( n )' 형식을 포함한 첫 부분을 삭제하고 저장합니다.

    :param input_file: 원본 텍스트 파일 경로
    :param output_file: 수정된 텍스트 파일 저장 경로
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 패턴 정의: ( ) 또는 ( n ) 형식
    pattern = r'^\s*\( *\)|^\s*\( *\d+ *\)'
    
    # 패턴에 해당하는 첫 번째 부분을 삭제
    match = re.search(pattern, content, flags=re.MULTILINE)
    if match:
        content = content[match.end():]  # 매칭된 부분 이후부터 유지

    # 수정된 내용을 새 파일로 저장
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

def process_folder(input_folder, output_folder):
    """
    폴더 내 모든 .txt 파일을 처리하여 '( )' 또는 '( n )' 형식을 포함한 첫 부분을 삭제하고 결과를 저장합니다.

    :param input_folder: 입력 폴더 경로
    :param output_folder: 출력 폴더 경로
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            process_file(input_path, output_path)

# 사용 예시
if __name__ == "__main__":
    input_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/4_2_1심의결과O/tail_remove"  # 입력 폴더 경로
    output_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/4_2_1심의결과O/tail_header_removed"  # 출력 폴더 경로

    process_folder(input_folder, output_folder)
