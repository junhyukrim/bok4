import pandas as pd
from ekonlpy.tag import Mecab
import csv

# CSV 파일 읽기
df = pd.read_csv('bond_cape_fixed.csv', encoding='utf-8-sig')

# Mecab 초기화
mecab = Mecab()

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

# 'original_sentence' 열에 대해 적용
df['pos_tagged'] = df['original_sentence'].apply(pos_tagging)
df['tokenized'] = df['original_sentence'].apply(only_tokens)

# CSV로 저장 (튜플 형태 유지)
output_path = 'sample_bond_cape_tokenized.csv'
df.to_csv(
    output_path,
    index=False,
    encoding='utf-8-sig',
    quoting=csv.QUOTE_NONE,  # 따옴표 없이 저장
    sep='|',                 # 구분자 변경
    escapechar='\\'          # 특수문자 처리
)

print(f":white_tick: {output_path} 저장 완료.")
print(df[['date', 'doc_id', 'sentence_id', 'original_sentence', 'tokenized', 'pos_tagged']].head())