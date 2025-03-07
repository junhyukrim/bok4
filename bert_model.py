import pandas as pd
from transformers import pipeline, AutoTokenizer

# 🔹 FinBERT 모델 & 토크나이저 로드
nlp = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone", return_all_scores=True)
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")

# 🔹 CSV 파일 불러오기 (전체 데이터)
file_path = r"C:\Users\likel\Desktop\bok\전처리\전처리_edaily.csv"
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 🔹 날짜 형식 변환
df['date'] = pd.to_datetime(df['date'])

# 🔹 감성 분석 결과 저장 리스트
results = []

# 🔹 긴 문장을 512 토큰 이하로 자르는 함수
def truncate_text(text, tokenizer, max_length=512):
    encoded = tokenizer.encode(text, truncation=True, max_length=max_length)
    truncated_text = tokenizer.decode(encoded, skip_special_tokens=True)
    return truncated_text

# 🔹 한 문장씩 감성 분석 수행
for index, row in df.iterrows():
    sentence = row['orgn_sntc']  # 원본 문장
    date = row['date']
    doc_id = row['doc_id']

    # ✅ 긴 문장 512 토큰 이하로 자르기
    truncated_sentence = truncate_text(sentence, tokenizer)

    # ✅ BERT 감성 분석 실행
    sentiment_results = nlp(truncated_sentence)[0]
    positive_score = sentiment_results[1]['score']  # 긍정 확률
    negative_score = sentiment_results[2]['score']  # 부정 확률

    # ✅ 최종 감성 점수 계산 (긍정 - 부정)
    sentiment_score = positive_score - negative_score

    # ✅ 결과 저장
    results.append({'date': date.date(), 'doc_id': doc_id, 'sentence_tone': sentiment_score})

    # 중간 진행 상태 확인 (1000개마다 출력)
    if (index + 1) % 1000 == 0:
        print(f"🔄 진행 중... {index + 1}/{len(df)}")

# 🔹 결과를 데이터프레임으로 변환
result_df = pd.DataFrame(results)

# 🔹 문서별 평균 감성 점수 계산
summary_df = result_df.groupby(['date', 'doc_id']).agg({'sentence_tone': 'mean'}).reset_index()

# 🔹 최종 결과 저장 (파일명 변경)
output_path = r"C:\Users\likel\Desktop\bok\bert모델\bert-edaily-감성분석.csv"
summary_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ 감성 분석 완료! 최종 요약 데이터 저장 완료:\n📁 {output_path}")
