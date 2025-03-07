import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 데이터 로드
file_path = "D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_converted.csv"
data = pd.read_csv(file_path)

# 'date' 열을 datetime 형식으로 변환
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

# 부호 일치 여부 계산 (1: 일치, 0: 불일치)
data['sign_match'] = np.sign(data['tone']) == np.sign(data['market_label'])

# 부호 일치율의 100일 이동 평균 계산
data['rolling_accuracy'] = data['sign_match'].rolling(window=100).mean()

# 그래프 그리기
plt.figure(figsize=(12, 6))
plt.plot(data['date'], data['rolling_accuracy'], label='100-Day Rolling Accuracy', color='blue')
plt.title('100-Day Rolling Accuracy (Tone vs Market Label)')
plt.xlabel('Date')
plt.ylabel('Accuracy')
plt.axhline(y=0.5, color='red', linestyle='--', label='Baseline (50%)')  # 기준선 추가
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()