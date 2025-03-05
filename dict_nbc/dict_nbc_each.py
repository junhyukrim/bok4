import os
import pandas as pd
from collections import defaultdict
import json

# 폴더 내 모든 CSV 파일 읽기 및 처리
def process_files_individually(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):  # CSV 파일만 처리
            file_path = os.path.join(folder_path, file_name)
            data = pd.read_csv(file_path)
            
            print(f"Calculating n-gram scores for {file_name}...")
            ngram_scores = calculate_ngram_scores(data)
            
            output_file = f"{os.path.splitext(file_name)[0]}_ngram_scores.json"
            print(f"Saving dictionary to {output_file}...")
            save_dictionaries(ngram_scores, os.path.join(folder_path, output_file))

# n-gram별 Hawkish/Dovish 점수 계산 (빈도 포함)
def calculate_ngram_scores(data):
    ngram_columns = ['1gram', '2gram', '3gram', '4gram', '5gram']
    ngram_scores = defaultdict(lambda: {'count': 0, 'score_sum': 0})
    
    for _, row in data.iterrows():
        market_label = row['market_label']  # 금리 변화 라벨
        for col in ngram_columns:
            if pd.notna(row[col]):  # 결측치 처리
                ngrams = row[col].split(", ")  # 쉼표로 구분된 n-grams
                for ngram in ngrams:
                    ngram_scores[ngram]['count'] += 1
                    ngram_scores[ngram]['score_sum'] += market_label
    
    # 각 n-gram의 평균 점수 계산
    for ngram, values in ngram_scores.items():
        values['score'] = values['score_sum'] / values['count']
    
    return ngram_scores

# 사전 생성 및 저장
def save_dictionaries(ngram_scores, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(ngram_scores, f, ensure_ascii=False, indent=4)

# 메인 실행 함수
def main(folder_path):
    print("Processing each file individually...")
    process_files_individually(folder_path)

# 실행 예제
if __name__ == "__main__":
    folder_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_ngram/labeled"  # CSV 파일이 담긴 폴더 경로
    main(folder_path)
