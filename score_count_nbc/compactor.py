import pandas as pd

# 함수: 열 필터링 및 순서 변경
def process_columns(input_path, output_path):
    # CSV 파일 로드
    df = pd.read_csv(input_path)

    # 필요한 열만 남기기
    columns_to_keep = [
        'doc_id', 'date', 'market_rate', 'base_rate', 'base_future', 
        'market_future', 'base_label', 'market_label', 
        'P_prime_hawkish', 'P_prime_neutral', 'P_prime_dovish', 'tone'
    ]
    df_filtered = df[columns_to_keep]

    # 열 순서 변경
    columns_order = [
        'date', 'market_rate', 'base_rate', 'base_future', 
        'market_future', 'base_label', 'market_label', 
        'tone', 'P_prime_hawkish', 'P_prime_neutral', 
        'P_prime_dovish', 'doc_id'
    ]
    df_reordered = df_filtered[columns_order]

    # 결과 저장
    df_reordered.to_csv(output_path, index=False)
    print(f"결과가 {output_path}에 저장되었습니다.")

# 실행 예시
input_path = 'D:/bok4_resource/analysis/all_analysis.csv'  # 입력 파일 경로
output_path = 'D:/bok4_resource/analysis/all_analysis_compact.csv'  # 출력 파일 경로
process_columns(input_path, output_path)
