import os
import pandas as pd

# CSV 파일 로드
csv_file = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_txt/bond_txt/test/typename_hyundai.csv"  # CSV 파일 경로
data = pd.read_csv(csv_file, header=None, names=["original", "new"])

# 텍스트 파일이 있는 폴더 경로 설정
folder_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_txt/bond_txt/test/input"  # 실제 폴더 경로로 변경하세요

# 파일 이름 변경 작업 수행
success_count = 0
failed_count = 0

for index, row in data.iterrows():
    original_file = os.path.join(folder_path, row["original"])
    new_file = os.path.join(folder_path, row["new"])
    
    try:
        if os.path.exists(original_file):
            os.rename(original_file, new_file)
            print(f"변경 성공: {row['original']} -> {row['new']}")
            success_count += 1
        else:
            print(f"파일 없음: {row['original']}")
            failed_count += 1
    except Exception as e:
        print(f"오류 발생 ({row['original']} -> {row['new']}): {e}")
        failed_count += 1

# 결과 요약 출력
print("\n작업 완료!")
print(f"성공적으로 변경된 파일: {success_count}")
print(f"실패한 파일: {failed_count}")
