import pandas as pd

def process_csv(file_path):
    # CSV 파일 읽기
    df = pd.read_csv(file_path)
    
    # `original_sentence` 값이 마침표(.) 하나만 포함된 행 제거
    df = df[df['original_sentence'] != '.']
    
    # `sentence_id`를 1부터 다시 재발급
    df['sentence_id'] = range(1, len(df) + 1)
    
    # 수정된 데이터프레임을 원래 파일에 덮어쓰기
    df.to_csv(file_path, index=False)
    print(f"File '{file_path}' has been successfully updated.")

# 실행 예시
file_path = 'C:/Users/egege/OneDrive/Documents/bok4_resource/bond_csv/bond_kiwoom.csv'  # 대상 파일 경로
process_csv(file_path)
