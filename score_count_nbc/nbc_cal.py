import pandas as pd
import math

# 함수: hawkish_sigma, neutral_sigma, dovish_sigma 계산
def calculate_sigmas(z_count_and_score, epsilon=1e-6):
    # 초기값 설정
    hawkish_sigma = 0
    neutral_sigma = 0
    dovish_sigma = 0

    # count_and_score가 비어 있는 경우 처리
    if not isinstance(z_count_and_score, str) or not z_count_and_score.strip():
        return hawkish_sigma, neutral_sigma, dovish_sigma

    # count_and_score 열 파싱 및 계산
    try:
        items = z_count_and_score.split('), (')  # 각 (count, score) 쌍 분리
        for item in items:
            item = item.replace('(', '').replace(')', '').strip()  # 괄호 제거 및 공백 제거
            z_count, score = map(float, item.split(','))  # count와 score 분리
            hawkish_sigma += math.log(max(epsilon, 1 + score)) * z_count
            neutral_sigma += math.log(max(epsilon, 1 - abs(score))) * z_count
            dovish_sigma += math.log(max(epsilon, 1 - score)) * z_count
    except Exception as e:
        print(f"파싱 오류: {e}, 데이터: {z_count_and_score}")

    return hawkish_sigma, neutral_sigma, dovish_sigma

# 함수: 로그 확률 및 정규화된 확률 계산
def calculate_probabilities(row, ppH, ppN, ppD):
    epsilon = 1e-6  # 안정성을 위한 작은 값
    
    # Sigma 값 가져오기
    hawkish_sigma = row.get('hawkish_sigma', 0)
    neutral_sigma = row.get('neutral_sigma', 0)
    dovish_sigma = row.get('dovish_sigma', 0)

    # Prior probabilities 설정
    logP_hawkish = math.log(ppH) + hawkish_sigma
    logP_neutral = math.log(ppN) + neutral_sigma
    logP_dovish = math.log(ppD) + dovish_sigma

    # 로그 확률 범위 제한 (math.exp() 안정성을 위해)
    logP_hawkish = min(max(logP_hawkish, -700),700)
    logP_neutral = min(max(logP_neutral, -700),700)
    logP_dovish = min(max(logP_dovish, -700),700)

    # 지수화하여 실제 확률 계산
    P_hawkish = math.exp(logP_hawkish)
    P_neutral = math.exp(logP_neutral)
    P_dovish = math.exp(logP_dovish)

    # 전체 확률 합산
    total_probability = P_hawkish + P_neutral + P_dovish

    # 정규화된 확률 계산
    P_prime_hawkish = P_hawkish / total_probability if total_probability > 0 else 0
    P_prime_neutral = P_neutral / total_probability if total_probability > 0 else 0
    P_prime_dovish = P_dovish / total_probability if total_probability > 0 else 0

    max_prob = max(P_prime_hawkish, P_prime_neutral, P_prime_dovish)
    if max_prob == P_prime_hawkish:
        tone = P_prime_hawkish
    elif max_prob == P_prime_neutral:
        tone = 0
    elif max_prob == P_prime_dovish:
        tone = -P_prime_dovish

    return pd.Series({
        'logP_hawkish': logP_hawkish,
        'logP_neutral': logP_neutral,
        'logP_dovish': logP_dovish,
        'P_prime_hawkish': P_prime_hawkish,
        'P_prime_neutral': P_prime_neutral,
        'P_prime_dovish': P_prime_dovish,
        'tone': tone
    })

# 메인 함수: 통합 처리
def process_all(input_path, output_path):
    # Prior probabilities 설정 (예시 값)
    ppH = 0.4532494738  # Prior probability for hawkish
    ppN = 0.1248557778  # Prior probability for neutral
    ppD = 0.4218947484  # Prior probability for dovish

    # CSV 파일 로드
    df = pd.read_csv(input_path)

    # Sigma 계산 및 새로운 열 추가 (hawkish_sigma, neutral_sigma, dovish_sigma)
    sigmas_df = df.apply(lambda row: pd.Series(calculate_sigmas(row.get('z_count_and_score', ''))), axis=1)
    sigmas_df.columns = ['hawkish_sigma', 'neutral_sigma', 'dovish_sigma']
    df = pd.concat([df, sigmas_df], axis=1)

    # 로그 확률 및 정규화된 확률 계산 및 새로운 열 추가 (logP_* 및 P_prime_*)
    probabilities_df = df.apply(lambda row: calculate_probabilities(row, ppH, ppN, ppD), axis=1)
    df = pd.concat([df, probabilities_df], axis=1)

    # 열 순서 재정렬 (count_and_score을 가장 우측으로 이동)
    columns_order = [col for col in df.columns if col != 'z_count_and_score'] + ['z_count_and_score']
    df = df[columns_order]

    # 결과 저장
    df.to_csv(output_path, index=False)
    print(f"결과가 {output_path}에 저장되었습니다.")


# 실행 예시
input_path = 'D:/bok4_resource/bok_minute/minute_z_score_compact.csv'  # 입력 파일 경로
output_path = 'D:/bok4_resource/bok_minute/minute_totalscore.csv'  # 출력 파일 경로
process_all(input_path, output_path)
