import pandas as pd
import os

def split_csv(input_file, output_folder, chunk_size):
    # CSV 파일 읽기
    df = pd.read_csv(input_file)
    
    # 출력 폴더 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 파일 이름에서 확장자 제거
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    
    # 분할 작업
    current_chunk = []
    current_size = 0
    file_index = 1
    
    for _, row in df.iterrows():
        current_chunk.append(row)
        current_size += 1
        
        # 다음 행의 doc_id가 현재 chunk와 충돌하지 않도록 확인
        if current_size >= chunk_size:
            next_index = _ + 1
            if next_index < len(df) and df.iloc[next_index]['doc_id'] != row['doc_id']:
                # 현재 chunk 저장
                output_file = os.path.join(output_folder, f"{base_filename}_chunk_{file_index}.csv")
                pd.DataFrame(current_chunk).to_csv(output_file, index=False)
                
                # 초기화
                current_chunk = []
                current_size = 0
                file_index += 1
    
    # 남아 있는 데이터 저장
    if current_chunk:
        output_file = os.path.join(output_folder, f"{base_filename}_chunk_{file_index}.csv")
        pd.DataFrame(current_chunk).to_csv(output_file, index=False)

# 실행 예시
input_csv = "D:/bok4_resource/analysis/all_analysis_for_ppt.csv"
output_dir = "D:/bok4_resource/analysis/all_analysis_for_ppt"
split_csv(input_csv, output_dir, chunk_size=10000)
