import os
import re

def remove_lines_without_korean(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 한글이 포함된 줄만 남김
    filtered_lines = [line for line in lines if re.search(r'[\u3131-\u3163\uac00-\ud7a3]', line)]

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(filtered_lines)

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            remove_lines_without_korean(input_path, output_path)

# 사용 예시
if __name__ == "__main__":
    input_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/4_1토의내용O_perioded"  # 입력 폴더 경로
    output_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/4_1토의내용O_perioded/nohangul_removed"  # 출력 폴더 경로

    process_folder(input_folder, output_folder)
