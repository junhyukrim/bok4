import pandas as pd

# 함수: 부호가 일치하는 행의 비율 계산
def calculate_matching_ratio(input_path):
    # CSV 파일 로드
    df = pd.read_csv(input_path)

    # market_label이 문자열인 경우 숫자로 변환 (예: 'hawkish'=1, 'neutral'=0, 'dovish'=-1)
    if df['market_label'].dtype == 'object':
        label_map = {'hawkish': 1, 'neutral': 0, 'dovish': -1}
        df['market_label_numeric'] = df['market_label'].map(label_map)
    else:
        df['market_label_numeric'] = df['market_label']

    # 부호가 일치하는 행 계산
    matching_rows = df[df['market_label_numeric'] * df['tone'] >= 0].shape[0]  # 부호가 일치하는 경우
    total_rows = df.shape[0]  # 전체 행 수

    # 비율 계산
    matching_ratio = matching_rows / total_rows if total_rows > 0 else 0

    print(f"전체 행 수: {total_rows}")
    print(f"부호가 일치하는 행 수: {matching_rows}")
    print(f"부호가 일치하는 행의 비율: {matching_ratio:.6f}")

    return matching_ratio

# 실행 예시
input_path = 'D:/bok4_resource/analysis/all_analysis_compact_bydate.csv'  # 입력 파일 경로
calculate_matching_ratio(input_path)
