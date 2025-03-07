import os
import re
import shutil

def split_file(input_file, output_folder):
    """
    텍스트 파일을 특정 패턴(<의안, 〈의안, <보고, 〈보고)으로 나누고 결과를 저장합니다.
    split되지 않은 경우 원본 파일을 그대로 저장합니다.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 파일을 나눌 패턴 정의
    split_pattern = r'(?=<의안|〈의안|<보고|〈보고)'
    parts = re.split(split_pattern, content)

    # 원본 파일명에서 확장자 제거
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # 나눠진 부분 저장
    if len(parts) > 1:  # 패턴이 존재하여 나눠진 경우
        for i, part in enumerate(parts, 1):
            if part.strip():  # 빈 부분 무시
                output_file = os.path.join(output_folder, f"{base_name}_{i}.txt")
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(part.strip())
    else:  # 패턴이 없어 split되지 않은 경우
        output_file = os.path.join(output_folder, f"{base_name}_original.txt")
        shutil.copy(input_file, output_file)

def process_folder(input_folder, output_folder):
    """
    폴더 내 모든 .txt 파일 처리: 특정 패턴으로 나누고 결과를 출력 폴더에 저장합니다.
    split되지 않은 경우 원본 파일을 그대로 저장합니다.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            split_file(input_path, output_folder)

# 사용 예시
if __name__ == "__main__":
    input_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/page_removed"
    output_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/split"
    process_folder(input_folder, output_folder)


