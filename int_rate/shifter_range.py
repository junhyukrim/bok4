import pandas as pd

# CSV 파일 읽기
input_csv_path = "D:/bok4_resource/int/merged_rates.csv"
output_csv_path = "D:/bok4_resource/int/merged_rates_with_1_28future.csv"

# 데이터 로드
data = pd.read_csv(input_csv_path)

# 1일부터 28일까지의 미래 금리 열 추가
for n in range(1, 29):  # 1일부터 28일까지
    data[f'market_future_{n}'] = data['market_rate'].shift(-n)

# 결과를 새로운 CSV 파일로 저장
data.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

print(f"결과가 {output_csv_path}에 저장되었습니다.")
