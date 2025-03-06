import pandas as pd
import glob
import os

# CSV 파일들이 있는 폴더 경로
folder_path = r"C:/Users/hp/Downloads/total_bond_csv"

# 폴더 내 모든 CSV 파일 경로 가져오기 (하위 폴더까지)
csv_files = glob.glob(os.path.join(folder_path, '**', '*.csv'), recursive=True)

# 데이터프레임 리스트
df_list = []

for file in csv_files:
    df = pd.read_csv(file, encoding='utf-8-sig')
    df_list.append(df)
    print(f"{file} 읽기 완료.")

# 모든 데이터프레임 합치기
final_df = pd.concat(df_list, ignore_index=True)

# 합친 파일 저장
output_path = os.path.join(folder_path, "merged_all.csv")
final_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ 모든 CSV 파일을 합쳐서 {output_path}에 저장 완료!")
