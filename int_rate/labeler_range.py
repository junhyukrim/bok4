import pandas as pd

# CSV 파일 경로
input_csv_path = "D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_1_28.csv"
output_csv_path = "D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_1_28_labeled.csv"

# 데이터 로드
data = pd.read_csv(input_csv_path)

# market_label 계산: market_future_n이 market_rate보다 높으면 1, 같으면 0, 낮으면 -1
for n in range(1, 29):
    data[f'market_label_{n}'] = data.apply(
        lambda row: 1 if row[f'market_future_{n}'] > row['market_rate_x'] 
                    else (0 if row[f'market_future_{n}'] == row['market_rate_x'] else -1),
        axis=1
    )

# 결과를 새로운 CSV 파일로 저장
data.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

print(f"결과가 {output_csv_path}에 저장되었습니다.")