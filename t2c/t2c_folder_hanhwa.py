import os
import re
import pandas as pd
from datetime import datetime


def process_txt_to_dataframe(file_path, replacement_dict, exception_list):
    # 파일명에서 날짜 추출 (예: "hanhwatujajeunggweon_101011_1.txt")
    file_name = os.path.basename(file_path)
    date_str = file_name.split('_')[1] if '_' in file_name else file_name.split('.')[0][-6:]  # Handle different filename formats
    try:
        date = datetime.strptime(date_str, '%y%m%d').strftime('%Y-%m-%d')  # "2010-10-11"
    except ValueError:
        # Fallback for cases where the date format is different
        date = "Unknown Date"
    
    # 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 규칙 1: (cid:{숫자}) 형태를 "."으로 대체
    content = re.sub(r'\(cid:\d+\)', '.', content)

    # 규칙 2: 소수점({숫자}.{숫자}) 표현에서 "." 제거
    content = re.sub(r'(\d)\.(\d)', r'\1\2', content)

    # 규칙 2.1: 모든 괄호 안의 내용을 괄호 포함 삭제
    content = re.sub(r'\(.*?\)', '', content)

    # 규칙 2.2: 모든 더블 스페이스를 싱글 스페이스로 변환
    content = re.sub(r'\s{2,}', ' ', content)

    lines = content.splitlines()
    
    # 첫 번째 패스: 작은따옴표로 시작하는 줄을 이전 줄과 병합
    i = 0
    while i < len(lines):
        if i > 0 and lines[i].strip().startswith("'"):
            lines[i-1] = lines[i-1].strip() + " " + lines[i].strip()
            lines.pop(i)
        else:
            i += 1
    
    # 두 번째 패스: 일반 규칙 적용
    processed_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 작은따옴표로 둘러싸인 단어 보호
        protected_words = re.findall(r"'[^']*'", line)
        for i, word in enumerate(protected_words):
            line = line.replace(word, f"PROTECTED_WORD_{i}")
        
        # 예외 리스트에 없는 특수 문자로 시작하는 줄 처리
        if line and line[0] not in exception_list and not re.match(r'^\w', line):
            line = re.sub(r'^[^\w\s]', '.', line)
        
        # 보호된 단어 복원
        for i, word in enumerate(protected_words):
            line = line.replace(f"PROTECTED_WORD_{i}", word)
        
        processed_lines.append(line)
    
    # 줄 결합 및 남은 처리
    combined_content = " ".join(processed_lines)
    
    # 규칙 3.2: 텍스트 전체가 "."으로 시작하면 해당 "."을 삭제
    if combined_content.startswith('.'):
        combined_content = combined_content[1:]
    
    # 규칙 3.3: 특정 딕셔너리를 적용하여 텍스트 변환
    for key, value in replacement_dict.items():
        combined_content = combined_content.replace(key, value)
    
    # 규칙 3.9: .이 연달아 2개 이상 나오는 경우 하나의 .으로 처리
    combined_content = re.sub(r'\.{2,}', '.', combined_content)
    
    # **추가 전처리**: 마침표 뒤에 공백 추가 (문장 분리를 위해)
    combined_content = re.sub(r'(?<!\s)\.', '. ', combined_content).strip()
    
    # 규칙 4: . ! ? 를 기준으로 문장을 나누기
    sentences = re.split(r'(?<=[.!?])\s+', combined_content)
    
    # DataFrame 생성
    data = []
    for idx, sentence in enumerate(sentences, start=1):
        if sentence.strip():  # 빈 문장은 제외
            data.append({
                'date': date,
                'doc_id': file_name,
                'sentence_id': idx,
                'original_sentence': sentence.strip()
            })
    
    return pd.DataFrame(data)


def process_folder_to_single_csv(input_folder, output_csv_path, replacement_dict, exception_list):
    all_dataframes = []

    # 폴더 내 모든 txt 파일 처리
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_folder, file_name)
            df = process_txt_to_dataframe(file_path, replacement_dict, exception_list)
            all_dataframes.append(df)

    # 모든 데이터프레임을 하나로 합치기
    if all_dataframes:
        final_dataframe = pd.concat(all_dataframes, ignore_index=True)
        
        # 단일 CSV 파일로 저장 (quotechar 설정 추가)
        final_dataframe.to_csv(output_csv_path, index=False, encoding='utf-8-sig', quotechar='"')
        
        print(f"통합 CSV 파일이 생성되었습니다: {output_csv_path}")
    else:
        print("처리할 파일이 없습니다.")


# 실행 예제
input_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/한화/0cleansed"  # TXT 파일들이 저장된 폴더 경로
output_csv_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/한화/0cleansed/hanhwa.csv"  # 통합된 CSV 파일 경로

# 딕셔너리 정의 (규칙 3.3 적용)
replacement_dict = {
    "vs.": "vs",
    "보임": "보임.",
    " 전 망한 ": " 전망한 "
}

# 예외 리스트 정의 (규칙 3에서 제외할 특수 문자들)
exception_list = ["'"]  # 예시: "'"는 규칙 3의 적용을 받지 않음

process_folder_to_single_csv(input_folder, output_csv_path, replacement_dict, exception_list)