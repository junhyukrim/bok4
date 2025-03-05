import pandas as pd
from ekonlpy.tag import Mecab
import csv

# CSV 파일 읽기
df = pd.read_csv('C:/Users/hp/Downloads/total_bond_csv/bond_merged/bond_merged.csv', encoding='utf-8-sig') # 불러들일 csv 파일 경로를 입력해주세요.

# Mecab 초기화
mecab = Mecab()

# 불용어 품사 설정
stop_pos = [
    'NR', 'MAJ', 'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ', 'JC', 'JK',
    'NNBC', 'SF', 'SE', 'SW', 'SH', 'SN', 'XSV', 'EP', 'EF', 'EC', 'ETN', 'ETM',
    'VCP', 'XSA', 'XSV', 'XSN', 'SSO'
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
    return [(word, pos) for word, pos in pos_tag s if pos in stop_pos]
    
# 클린 토큰 함수(불용어 제외)
def clean_tokens(pos_tags):
    return [word for word, pos in pos_tags if pos not in stop_pos]

# 열에 대해 적용
df['tokenized'] = df['original_sentence'].apply(only_tokens)
df['pos_tagged'] = df['original_sentence'].apply(pos_tagging)
df['stopword_tokens'] = df['pos_tagged'].apply(extract_stopwords)
# df['cleaned_tokens'] = df['pos_tagged'].apply(clean_tokens)

# CSV로 저장 (튜플 형태 유지)
output_path = 'C:/Users/hp/Downloads/total_bond_csv/bond_merged/tokenized_total_bond_temp.csv' # csv 파일 이름 설정 및 경로를 적어주세요.
df.to_csv(
    output_path,
    index=False,
    encoding='utf-8-sig',
    quoting=csv.QUOTE_MINIMAL,  # 따옴표 자동 처리
    sep=','
)

print(f":white_tick: {output_path} 저장 완료.")
print(df[['date', 'doc_id', 'sentence_id', 'original_sentence', 'tokenized', 'pos_tagged', 'stopword_tokens', 'cleaned_tokens']].head())

#, 'cleaned_tokens'