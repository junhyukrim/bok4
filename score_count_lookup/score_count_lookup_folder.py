import pandas as pd
import json
import os

# JSON 사전 로드
with open('D:/bok4_resource/score_count/sample/final_dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

# CSV 파일이 있는 폴더 경로
input_folder_path = 'D:/bok4_resource/score_count/sample'
output_folder_path = 'D:/bok4_resource/score_count/sample/output'

# output 폴더가 없으면 생성
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# n-gram 칼럼 리스트 (예: 1gram, 2gram, ..., 5gram)
ngram_columns = ['1gram', '2gram', '3gram', '4gram', '5gram']

# count_and_score 칼럼 생성 함수
def calculate_count_and_score(row):
    result = []
    for col in ngram_columns:
        if col in row and isinstance(row[col], str):
            ngrams = row[col].split(',')  # 쉼표로 분리된 n-grams
            for ngram in ngrams:
                ngram = ngram.strip()  # 공백 제거
                if ngram in dictionary:
                    count = dictionary[ngram]['count']
                    score = dictionary[ngram]['score']
                    result.append(f"({count},{score})")
                
    return ', '.join(result)

# 폴더 내 모든 CSV 파일 처리
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.csv'):  # CSV 파일만 처리
        input_file_path = os.path.join(input_folder_path, file_name)
        output_file_path = os.path.join(output_folder_path, f"processed_{file_name}")
        
        # CSV 파일 로드
        df = pd.read_csv(input_file_path)
        
        # count_and_score 칼럼 추가
        df['count_and_score'] = df.apply(calculate_count_and_score, axis=1)
        
        # 결과 저장
        df.to_csv(output_file_path, index=False)
        print(f"{file_name} 처리 완료. 결과가 {output_file_path}에 저장되었습니다.")
