import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt


# 데이터 로드
data = pd.read_csv('D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_1_28_labeled.csv')

# NaN 및 무한값 처리
data = data.replace([np.inf, -np.inf], np.nan)  # 무한값을 NaN으로 변환
data = data.dropna()  # NaN 값이 포함된 행 제거

# 상관분석

for n in range(1, 29):
    correlation = data['tone'].corr(data[f'market_label_{n}'])
    print(f"Tone과 Market Label {n} 간의 상관계수: {correlation}")



# # 회귀 성능 평가
# mse = mean_squared_error(data['market_rate'], data['tone'])
# r2 = r2_score(data['market_rate'], data['tone'])
# print(f"MSE (평균 제곱 오차): {mse}")
# print(f"R² 점수: {r2}")

# mse = mean_squared_error(data['market_future'], data['tone'])
# r2 = r2_score(data['market_future'], data['tone'])
# print(f"MSE (평균 제곱 오차): {mse}")
# print(f"R² 점수: {r2}")

# mse = mean_squared_error(data['market_label'], data['tone'])
# r2 = r2_score(data['market_label'], data['tone'])
# print(f"MSE (평균 제곱 오차): {mse}")
# print(f"R² 점수: {r2}")



# # 분류 정확도 평가
# accuracy = accuracy_score(data['market_label'], np.sign(data['tone']))
# precision = precision_score(data['market_label'], np.sign(data['tone']), average='weighted')
# recall = recall_score(data['market_label'], np.sign(data['tone']), average='weighted')
# f1 = f1_score(data['market_label'], np.sign(data['tone']), average='weighted')

# print(f"정확도: {accuracy}")
# print(f"정밀도: {precision}")
# print(f"재현율: {recall}")
# print(f"F1 점수: {f1}")