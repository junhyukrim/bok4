import pandas as pd

# 함수: 열 삭제 및 동일한 date 값의 처리
def process_data(input_path, output_path):
    # CSV 파일 로드
    df = pd.read_csv(input_path)

    # 1. 필요 없는 열 삭제
    columns_to_drop = ['P_prime_hawkish', 'P_prime_neutral', 'P_prime_dovish', 'doc_id']
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # 2. 동일한 date 값에 대해 처리
    # 숫자형 열은 평균값으로, 비숫자형 열은 첫 번째 값으로 대체
    df_grouped = df.groupby('date', as_index=False).agg({
        'market_rate': 'first',  # 동일한 값이므로 첫 번째 값 사용
        'base_rate': 'first',
        'base_future': 'first',
        'market_future': 'first',
        'base_label': 'first',  # 동일한 값이므로 첫 번째 값 사용
        'market_label': 'first',
        'tone': 'mean'          # tone은 평균값 계산
    })

    # 결과 저장
    df_grouped.to_csv(output_path, index=False)
    print(f"결과가 {output_path}에 저장되었습니다.")

# 실행 예시
input_path = 'D:/bok4_resource/analysis/all_analysis_compact.csv'  # 입력 파일 경로
output_path = 'D:/bok4_resource/analysis/all_analysis_compact_bydate.csv'  # 출력 파일 경로
process_data(input_path, output_path)
