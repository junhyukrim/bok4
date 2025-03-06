import pandas as pd

# CSV 파일 경로
input_csv_path = "merged_rates_with_future.csv"
output_csv_path = "labeled_rates.csv"

# 데이터 로드
data = pd.read_csv(input_csv_path)

# base_label 계산: base_future가 base_rate보다 높으면 1, 같으면 0, 낮으면 -1
data['base_label'] = data.apply(
    lambda row: 1 if row['base_future'] > row['base_rate'] else (0 if row['base_future'] == row['base_rate'] else -1),
    axis=1
)

# market_label 계산: market_future가 market_rate보다 높으면 1, 같으면 0, 낮으면 -1
data['market_label'] = data.apply(
    lambda row: 1 if row['market_future'] > row['market_rate'] else (0 if row['market_future'] == row['market_rate'] else -1),
    axis=1
)

# 결과를 새로운 CSV 파일로 저장
data.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

print(f"결과가 {output_csv_path}에 저장되었습니다.")
