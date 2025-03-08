import pandas as pd

# 함수: count 값을 정규화하여 (z-count, score) 생성
def normalize_counts(count_and_score):
    if not isinstance(count_and_score, str) or not count_and_score.strip():
        return ""  # 비어 있는 경우 처리

    try:
        # count 값 추출 및 총합 계산
        items = count_and_score.split('), (')
        counts = [float(item.split(',')[0].replace('(', '').replace(')', '').strip()) for item in items]
        total_count = sum(counts)

        # 정규화된 (z-count, score) 생성
        normalized_items = []
        for item in items:
            item = item.replace('(', '').replace(')', '').strip()
            count, score = map(float, item.split(','))
            z_count = count / total_count if total_count > 0 else 0  # 정규화
            normalized_items.append(f"({z_count:.6f},{score})")

        return ", ".join(normalized_items)
    except Exception as e:
        print(f"파싱 오류: {e}, 데이터: {count_and_score}")
        return ""

# 메인 함수
def process_normalization(input_path, output_path):
    # CSV 파일 로드
    df = pd.read_csv(input_path)

    # (z-count, score) 열 생성
    df['z_count_and_score'] = df['count_and_score'].apply(normalize_counts)

    # 결과 저장
    df.to_csv(output_path, index=False)
    print(f"결과가 {output_path}에 저장되었습니다.")

# 실행 예시
input_path = 'D:/bok4_resource/bok_minute/minute_score.csv'  # 입력 파일 경로
output_path = 'D:/bok4_resource/bok_minute/minute_z_score.csv'  # 출력 파일 경로
process_normalization(input_path, output_path)
