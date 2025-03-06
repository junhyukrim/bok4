import pandas as pd
import math

# CSV 파일 로드
csv_file_path = 'D:/bok4_resource/score_count/sample/output_with_count_and_score.csv'  # CSV 파일 경로
df = pd.read_csv(csv_file_path)

# Prior Probability 값 설정 (예시 값)
ppH = 0.3  # Prior Probability for hawkish
ppN = 0.4  # Prior Probability for neutral
ppD = 0.3  # Prior Probability for dovish

epsilon = 1e-6  # 안정성을 위한 작은 값

# log P 계산 함수
def calculate_log_probabilities(count_and_score_list, ppH, ppN, ppD, epsilon):
    logP_hawkish = math.log(ppH)
    logP_neutral = math.log(ppN)
    logP_dovish = math.log(ppD)

    for item in count_and_score_list:
        count, score = item
        logP_hawkish += math.log(max(epsilon, 1 + score)) * count
        logP_neutral += math.log(max(epsilon, 1 - abs(score))) * count
        logP_dovish += math.log(max(epsilon, 1 - score)) * count

    return logP_hawkish, logP_neutral, logP_dovish

# doc_id별 톤 계산 함수
def calculate_tones_for_doc(doc_group):
    count_and_score_list = []
    for _, row in doc_group.iterrows():
        count_and_score_items = row['count_and_score'].split(',')
        for item in count_and_score_items:
            item = item.strip()
            if item.startswith('(') and item.endswith(')'):
                count, score = map(float, item[1:-1].split(','))
                count_and_score_list.append((count, score))

    # 로그 확률 계산
    logP_hawkish, logP_neutral, logP_dovish = calculate_log_probabilities(count_and_score_list, ppH, ppN, ppD, epsilon)

    # 지수화 및 정규화
    P_hawkish = math.exp(logP_hawkish)
    P_neutral = math.exp(logP_neutral)
    P_dovish = math.exp(logP_dovish)

    total_probability = P_hawkish + P_neutral + P_dovish

    toneH = P_hawkish / total_probability
    toneN = P_neutral / total_probability
    toneD = P_dovish / total_probability

    return pd.Series({'toneH': toneH, 'toneN': toneN, 'toneD': toneD})

# doc_id별 그룹화 및 톤 계산
result_df = df.groupby('doc_id').apply(calculate_tones_for_doc).reset_index()

# 필요한 열만 남기기
columns_to_keep = ['date', 'market_rate', 'base_rate', 'base_future', 'market_future',
                   'base_label', 'market_label', 'doc_id']
final_df = df[columns_to_keep].drop_duplicates(subset='doc_id').merge(result_df, on='doc_id')

# 결과 저장
output_file_path = 'output_with_doc_tones.csv'
final_df.to_csv(output_file_path, index=False)
print(f"결과가 {output_file_path}에 저장되었습니다.")
