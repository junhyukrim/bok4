import pandas as pd

# CSV 파일 읽기
input_csv_path = "merged_rates.csv"
output_csv_path = "merged_rates_with_future.csv"

# 데이터 로드
data = pd.read_csv(input_csv_path)

# 3일 뒤의 base_rate 값을 추가
data['base_future'] = data['base_rate'].shift(-28)
data['market_future'] = data['market_rate'].shift(-28)

# 결과를 새로운 CSV 파일로 저장
data.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

print(f"결과가 {output_csv_path}에 저장되었습니다.")
