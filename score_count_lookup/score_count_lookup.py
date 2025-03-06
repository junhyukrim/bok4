import pandas as pd
import json

# JSON 사전 로드
with open('D:/bok4_resource/score_count/sample/final_dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

# CSV 파일 로드
csv_file_path = 'D:/bok4_resource/score_count/sample/labeled_processed_파이낸셜_clean_tokenized_chunk_125.csv'  # CSV 파일 경로
df = pd.read_csv(csv_file_path)

# n-gram 칼럼 리스트 (예: 1gram, 2gram, ..., 5gram)
ngram_columns = ['1gram', '2gram', '3gram', '4gram', '5gram']

# count_and_score 칼럼 생성
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

df['count_and_score'] = df.apply(calculate_count_and_score, axis=1)

# 결과 저장
output_file_path = 'D:/bok4_resource/score_count/sample/output_with_count_and_score.csv'
df.to_csv(output_file_path, index=False)
print(f"결과가 {output_file_path}에 저장되었습니다.")
