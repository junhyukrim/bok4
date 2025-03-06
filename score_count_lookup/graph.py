import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# CSV 파일 로드
file_path = 'D:/bok4_resource/analysis/all_analysis_compact_bydate.csv'
df = pd.read_csv(file_path)

# date 열을 datetime 형식으로 변환
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# 그래프 생성
fig, ax1 = plt.subplots(figsize=(15, 8))

# x축 설정
ax1.set_xlabel('Date')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# 첫 번째 y축 (tone)
ax1.set_ylabel('Tone', color='tab:blue')
ax1.plot(df['date'], df['tone'], color='tab:blue', marker='o', linestyle='-', label='Tone')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 두 번째 y축 (market_label)
ax2 = ax1.twinx()
ax2.set_ylabel('Marker Rate', color='tab:red')

# market_label이 문자열인 경우 숫자로 변환 (예: 'hawkish'=1, 'neutral'=0, 'dovish'=-1)
if df['market_rate'].dtype == 'object':
    label_map = {'hawkish': 1, 'neutral': 0, 'dovish': -1}
    df['market_label_numeric'] = df['market_rate'].map(label_map)
    ax2.plot(df['date'], df['market_label_numeric'], color='tab:red', marker='x', linestyle='--', label='Marker Rate')
    ax2.set_yticks([-1, 0, 1])
    ax2.set_yticklabels(['Dovish', 'Neutral', 'Hawkish'])
else:
    # market_label이 이미 숫자인 경우
    ax2.plot(df['date'], df['market_rate'], color='tab:red', marker='x', linestyle='--', label='Marker Rate')
ax2.tick_params(axis='y', labelcolor='tab:red')

# 제목 설정
plt.title('Tone and Market Label over Time')

# 범례 표시
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

# 그리드 추가
ax1.grid(True, alpha=0.3)

# 그래프 저장 및 표시
plt.tight_layout()
plt.savefig('tone_vs_market_label.png', dpi=300)
plt.show()
