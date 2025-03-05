import pandas as pd
import re
import os

def extract_date(doc_id):
    match_8_digits = re.search(r'(\d{8})', doc_id)
    if match_8_digits:
        return match_8_digits.group(1)
    match_6_digits = re.search(r'(\d{6})', doc_id)
    if match_6_digits:
        return '20' + match_6_digits.group(1)
    return None

# CSV 파일이 있는 폴더 경로
folder_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_ngram/ngram_sperated"

# 폴더 내의 모든 CSV 파일에 대해 처리
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        # CSV 파일 읽기
        data = pd.read_csv(file_path)
        
        # 'doc_id' 열에서 날짜 추출하여 'date' 열 업데이트
        data['date'] = data['doc_id'].apply(extract_date)
        
        # 수정된 데이터를 원본 파일에 덮어쓰기
        data.to_csv(file_path, index=False)
        
        print(f"{filename} 파일이 성공적으로 업데이트되었습니다.")

print("모든 CSV 파일의 처리가 완료되었습니다.")


