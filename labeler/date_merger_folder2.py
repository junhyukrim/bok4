import pandas as pd
import os

# 파일 경로
a_path = "labeled_rates.csv"
b_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_ngram/ngram_sperated"  # CSV 파일들이 있는 폴더 경로
output_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_ngram/labeled"  # 결과를 저장할 폴더 경로

try:
    # CSV 파일 읽기
    call_rate_df = pd.read_csv(a_path)

    # 'date' 열을 datetime 형식으로 변환
    call_rate_df['date'] = pd.to_datetime(call_rate_df['date'])

    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # b_folder 내의 모든 CSV 파일에 대해 처리
    for filename in os.listdir(b_folder):
        if filename.endswith(".csv"):
            b_path = os.path.join(b_folder, filename)
            base_rate_df = pd.read_csv(b_path)

            # 'date' 열을 datetime 형식으로 변환
            base_rate_df['date'] = pd.to_datetime(base_rate_df['date'])

            # 두 데이터프레임을 'date' 기준으로 병합 (가장 가까운 날짜를 찾음)
            merged_df = pd.merge_asof(base_rate_df.sort_values('date'), 
                                      call_rate_df.sort_values('date'), 
                                      on="date", 
                                      direction="nearest")

            # 병합 결과가 비어 있는지 확인
            if merged_df.empty:
                print(f"{filename}에 대해 병합 결과가 없습니다. 건너뜁니다.")
                continue

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
