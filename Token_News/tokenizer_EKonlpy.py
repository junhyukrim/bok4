import pandas as pd
from ekonlpy.tag import Mecab
import csv
import os

# CSV 파일이 있는 폴더 경로
input_folder = "C:/Users/hp/Downloads/total_bond_csv/bond_merged/"
output_folder = 'C:/Users/hp/Downloads/total_bond_csv/bond_merged/'

# output 폴더 없으면 생성
os.makedirs(output_folder, exist_ok=True)

# Mecab 초기화
mecab = Mecab()

# 불용어 품사 설정
stop_pos = [
    'NR', 'MAJ', 'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JC', 'JK',
    'NNBC', 'SF', 'SE', 'SW', 'SH', 'SN', 'XSV', 'EP', 'EF', 'EC', 'ETN', 'ETM',
    'VCP', 'XSA', 'XSV', 'XSN', 'SSO', 'JX','EX', 'UNKNOWN', 'SY', 'SC', 'SSC', 'NP', 'MP'
    'NNB', 'MM'
]

# 품사 태깅 함수
def pos_tagging(text):
    if not isinstance(text, str) or text.strip() == "":
        return []
    return mecab.pos(text)

# 토큰만 추출하는 함수
def only_tokens(text):
    if not isinstance(text, str) or text.strip() == "":
        return []
    return [word for word, pos in mecab.pos(text)]

# 불용어 태그 추출 함수
def extract_stopwords(pos_tags):
    return [(word, pos) for (word, pos) in pos_tags if pos in stop_pos]
    
# 클린 토큰 함수(불용어 제외)
def clean_tokens(pos_tags):
    return [(word, pos) for (word, pos) in pos_tags if pos not in stop_pos]

for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        print(f'처리 중: {filename}')

        # CSV 파일 읽기
        df = pd.read_csv(file_path, encoding='utf-8-sig')

        # 열에 대해 적용
        # df['tokenized'] = df['original_sentence'].apply(only_tokens)
        df['pos_tagged'] = df['original_sentence'].apply(pos_tagging)
        # df['stopword_tokens'] = df['pos_tagged'].apply(extract_stopwords)
        df['cleaned_tokens'] = df['pos_tagged'].apply(clean_tokens)

        # 파일명 변경 후 저장
        output_filename = filename.replace('.csv', '_clean_tokenized.csv')
        output_path = os.path.join(output_folder, output_filename)
        df.to_csv(
            output_path,
            index=False,
            encoding='utf-8-sig',
            quoting=csv.QUOTE_MINIMAL,  # 따옴표 자동 처리
            sep=','
        )
        print(f'{output_filename} 저장 완료')

# print(df[['date', 'doc_id', 'sentence_id', 'original_sentence', 'tokenized', 'pos_tagged', 'stopword_tokens', 'cleaned_tokens']].head())