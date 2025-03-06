import pandas as pd

# 입력 파일 경로
input_file_path = 'D:/bok4_resource/score_count/sample/output_with_count_and_score.csv'  # 첨부된 CSV 파일 경로
output_file_path = 'D:/bok4_resource/score_count/sample/cleaned_aggregated_output.csv'  # 출력 파일 경로

def clean_and_aggregate(input_csv, output_csv):
    """
    doc_id별로 데이터를 그룹화하고 필요한 열만 유지하며, count_and_score에서 빈 쉼표를 제거한 후 새로운 CSV 파일로 저장합니다.

    Parameters:
        input_csv (str): 입력 CSV 파일 경로
        output_csv (str): 출력 CSV 파일 경로
    """
    # CSV 데이터 로드
    df = pd.read_csv(input_csv)

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
    aggregated_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"결과가 {output_csv}에 저장되었습니다.")

# 실행
clean_and_aggregate(input_file_path, output_file_path)
