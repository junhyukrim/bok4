import pandas as pd

# 파일 경로
a_path = "D:/bok4_resource/int/merged_rates_with_1_28future.csv"
b_path = "D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_copy.csv"
output_path = "D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_1_28.csv"

try:
    # CSV 파일 읽기
    call_rate_df = pd.read_csv(a_path)
    base_rate_df = pd.read_csv(b_path)

    # 'date' 열을 기준으로 병합 (inner join)
    merged_df = pd.merge(call_rate_df, base_rate_df, on="date", how="inner")

    # 병합된 데이터 저장
    merged_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"병합된 데이터가 {output_path}에 저장되었습니다.")

except FileNotFoundError as e:
    print(f"파일을 찾을 수 없습니다: {e}")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
