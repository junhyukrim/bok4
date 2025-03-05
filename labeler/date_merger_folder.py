import pandas as pd
import os

# 파일 경로
a_path = "labeled_rates.csv"
b_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_ngram/ngram_sperated"  # CSV 파일들이 있는 폴더 경로
output_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_ngram/labeled"  # 결과를 저장할 폴더 경로

try:
    # CSV 파일 읽기
    call_rate_df = pd.read_csv(a_path)

    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # b_folder 내의 모든 CSV 파일에 대해 처리
    for filename in os.listdir(b_folder):
        if filename.endswith(".csv"):
            b_path = os.path.join(b_folder, filename)
            base_rate_df = pd.read_csv(b_path)

            # 'date' 열을 기준으로 병합 (inner join)
            merged_df = pd.merge(call_rate_df, base_rate_df, on="date", how="inner")

            # 병합된 데이터 저장
            output_filename = f"labeled_{filename}"
            output_path = os.path.join(output_folder, output_filename)
            merged_df.to_csv(output_path, index=False, encoding="utf-8-sig")
            print(f"{filename}에 대한 병합된 데이터가 {output_path}에 저장되었습니다.")

    print("모든 파일 처리가 완료되었습니다.")

except FileNotFoundError as e:
    print(f"파일 또는 폴더를 찾을 수 없습니다: {e}")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
