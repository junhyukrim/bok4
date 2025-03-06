import pandas as pd
import os

def clean_and_aggregate_folder(input_folder, output_folder):
    """
    폴더 내 모든 CSV 파일에 대해 doc_id별로 데이터를 그룹화하고,
    필요한 열만 유지하며 count_and_score에서 빈 쉼표를 제거한 후 새로운 CSV 파일로 저장합니다.

    Parameters:
        input_folder (str): 입력 CSV 파일이 있는 폴더 경로
        output_folder (str): 출력 CSV 파일을 저장할 폴더 경로
    """
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 폴더 내 모든 CSV 파일 처리
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):  # CSV 파일만 처리
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, f"cleaned_{file_name}")

            # CSV 데이터 로드
            df = pd.read_csv(input_file_path)

            # 필요한 열만 유지
            columns_to_keep = ['date', 'market_rate', 'base_rate', 'base_future', 'market_future', 
                               'base_label', 'market_label', 'doc_id', 'count_and_score']
            df = df[columns_to_keep]

            # count_and_score 열의 빈 쉼표 제거
            df['count_and_score'] = df['count_and_score'].str.replace(r',\s*,', ',', regex=True).str.strip(',')

            # doc_id별 데이터 그룹화 및 결합 (중복 제거)
            aggregated_df = df.groupby(['doc_id'], as_index=False).agg({
                'date': 'first',
                'market_rate': 'first',
                'base_rate': 'first',
                'base_future': 'first',
                'market_future': 'first',
                'base_label': 'first',
                'market_label': 'first',
                'count_and_score': lambda x: ', '.join(x.dropna().unique())
            })

            # 결과를 새로운 CSV 파일로 저장
            aggregated_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
            print(f"{file_name} 처리 완료. 결과가 {output_file_path}에 저장되었습니다.")

# 실행 예시
input_folder_path = 'D:/bok4_resource/score_count/sample/input_csv'  # 입력 폴더 경로
output_folder_path = 'D:/bok4_resource/score_count/sample/output_csv'  # 출력 폴더 경로

clean_and_aggregate_folder(input_folder_path, output_folder_path)
