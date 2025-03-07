import pandas as pd
import ast
from itertools import islice

def generate_ngrams(tokens, n):
    """
    Generate n-grams from a list of tokens.
    """
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def process_csv(input_file, output_file):
    # CSV 파일 읽기
    df = pd.read_csv(input_file)

    # pos_tagged 열에서 문자열을 리스트로 변환
    df['pos_tagged_list'] = df['cleaned_tokens'].apply(lambda x: [f"{word}/{tag}" for word, tag in ast.literal_eval(x)])

    # 1-gram부터 5-gram까지 생성
    for n in range(1, 6):
        col_name = f"{n}gram"
        df[col_name] = df['pos_tagged_list'].apply(lambda tokens: generate_ngrams(tokens, n))

    # 각 n-gram 열을 문자열로 변환 (CSV 저장을 위해)
    for n in range(1, 6):
        col_name = f"{n}gram"
        df[col_name] = df[col_name].apply(lambda x: ', '.join(x))

    # 불필요한 중간 열 제거
    df.drop(columns=['pos_tagged_list'], inplace=True)

    # 결과를 새로운 CSV 파일로 저장
    df.to_csv(output_file, index=False)

# 실행 예시
input_csv = "D:/bok4_resource/bok_minute/minute_token.csv"
output_csv = "D:/bok4_resource/bok_minute/minute_ngram.csv"
process_csv(input_csv, output_csv)
