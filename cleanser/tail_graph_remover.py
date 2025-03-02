import os
import re

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()  # 파일 전체를 읽음

    # 1. '자료:'가 포함된 줄 삭제
    lines = content.splitlines()
    lines = [line for line in lines if '자료:' not in line]
    
    # 줄 단위로 다시 합침
    content = '\n'.join(lines)

    # 1.5 리스트에 포함된 특정 단어 삭제
    words_to_remove = ['Dur.']  # 여기에 삭제할 단어를 추가
    for word in words_to_remove:
        content = content.replace(word, '')

    # 2. 숫자와 숫자 사이의 '.' 삭제
    content = re.sub(r'(?<=\d)\.(?=\d)', '', content)

    # 3. 문장 전체에서 마지막 '.' 이후의 모든 글 삭제
    if '.' in content:
        content = content[:content.rfind('.') + 1]  # 마지막 '.'까지만 남김

    # 결과를 새로운 파일에 저장
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content.strip())  # 앞뒤 공백 제거 후 저장

def process_folder(input_folder, output_folder):
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 입력 폴더 내 모든 .txt 파일 처리
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):  # .txt 파일만 처리
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            process_file(input_file_path, output_file_path)
            print(f"Processed: {filename}")

# 실행 예제
input_folder = 'C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/한화/bond_breif/txted'  # 처리할 파일이 들어있는 폴더 경로
output_folder = 'C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/한화/bond_breif/txted/tailcrop'  # 처리된 파일이 저장될 폴더 경로
process_folder(input_folder, output_folder)
