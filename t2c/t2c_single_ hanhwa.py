import re
import pandas as pd
from datetime import datetime

def process_txt_to_csv(file_path):
    # 파일명에서 날짜 추출 (예: "hanhwatujajeunggweon_101011_1.txt")
    file_name = file_path.split('/')[-1]
    date_str = file_name.split('_')[1]  # "101011"
    date = datetime.strptime(date_str, '%y%m%d').strftime('%Y-%m-%d')  # "2010-10-11"
    
    # 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 규칙 1: (cid:{숫자}) 형태를 "."으로 대체
    content = re.sub(r'\(cid:\d+\)', '.', content)
    
    # 규칙 2: 소수점({숫자}.{숫자}) 표현에서 "." 제거
    content = re.sub(r'(\d)\.(\d)', r'\1\2', content)
    
    # 규칙 3: 한 줄의 시작이 특수 문자로 시작하면 "."으로 대체
    lines = content.splitlines()
    processed_lines = []
    for line in lines:
        processed_lines.append(re.sub(r'^[^\w\s]', '.', line))
    content = '\n'.join(processed_lines)
    
    # 규칙 3.1: 모든 줄바꿈을 없앤다
    content = content.replace('\n', '').replace('\r', '')

    # 규칙 3.2: 텍스트 전체가 "."으로 시작하면 해당 "."을 삭제
    if content.startswith('.'):
        content = content[1:]
        
    # 규칙 4: . ! ? 를 기준으로 문장을 나누기
    sentences = re.split(r'(?<=[.!?])\s+', content)
    
    # CSV 데이터 생성
    data = []
    for idx, sentence in enumerate(sentences, start=1):
        if sentence.strip():  # 빈 문장은 제외
            data.append({
                'date': date,
                'doc_id': file_name,
                'sentence_id': idx,
                'original_sentence': sentence.strip()
            })
    
    # DataFrame 생성 및 CSV로 저장
    df = pd.DataFrame(data)
    output_csv_path = file_name.replace('.txt', '.csv')
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    
    print(f"CSV 파일이 생성되었습니다: {output_csv_path}")

# 실행 예제
file_path = "한화투자증권_101011_1.txt"
process_txt_to_csv(file_path)
