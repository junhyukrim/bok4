import pandas as pd
from nltk import ngrams, word_tokenize
import nltk

# NLTK 데이터 다운로드 (최초 실행 시 필요)
nltk.download('punkt')

# ✅ CSV 파일 읽기
df = pd.read_csv('bond_cape_tokenized.csv', encoding='utf-8-sig')

# ✅ n-grams 생성 함수
def generate_ngrams(text, n):
    if not isinstance(text, str) or text.strip() == "":
        return []
    tokens = word_tokenize(text)  # 단어 토큰화
    return list(ngrams(tokens, n))

# ✅ 각 n-grams 생성 및 데이터프레임에 추가
df['1_gram'] = df['original_sentence'].apply(lambda x: generate_ngrams(x, 1))
df['2_gram'] = df['original_sentence'].apply(lambda x: generate_ngrams(x, 2))
df['3_gram'] = df['original_sentence'].apply(lambda x: generate_ngrams(x, 3))
df['4_gram'] = df['original_sentence'].apply(lambda x: generate_ngrams(x, 4))
df['5_gram'] = df['original_sentence'].apply(lambda x: generate_ngrams(x, 5))

# ✅ 결과를 CSV 파일로 저장
output_path = 'bond_cape_with_ngrams.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"✅ {output_path} 저장 완료.")
print(df[['original_sentence', '1_gram', '2_gram', '3_gram', '4_gram', '5_gram']].head())