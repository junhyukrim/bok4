import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
file_path = "C:/Users/hp/Downloads/기사수_통합.csv"
df = pd.read_csv(file_path)

# 연도 컬럼 추가
df['year'] = df['year_month'].astype(str).str[:4]

# 뉴스 데이터 필터링
news_df = df[df['언론사'].isin(['asia_e', 'financial', 'money', 'edaily'])]

# 언론사별 연도별 합계 피벗테이블 생성
pivot = news_df.pivot_table(index='year', columns='언론사', values='article_count', aggfunc='sum', fill_value=0)

# 연도별 합계 계산 (4개사 합계)
pivot['total'] = pivot.sum(axis=1)

# 누적 합계 계산 (꺾은선 그래프 용)
pivot['cum_total'] = pivot['total'].cumsum()

# 색상 지정
color_dict = {
    'asia_e': '#833bee',       # 보라색
    'financial': '#fbb62a',  # 노란색
    'money': '#42c4a6',      # 초록색
    'edaily': '#ff3131',     # 빨간색
    'line': '#38b6ff'        # 누적 총합 꺾은선 (하늘색)
}

# 시각화
fig, ax1 = plt.subplots(figsize=(14, 8))

fig.patch.set_facecolor('black')  # 전체 배경
ax1.set_facecolor('black')        # 막대그래프 배경
ax2 = ax1.twinx()
ax2.set_facecolor('black')        # 꺾은선 그래프 배경

# 언론사별 누적 막대그래프
pivot[['asia_e', 'financial', 'money', 'edaily']].plot(
    kind='bar', stacked=True, ax=ax1, alpha=0.8, color=[color_dict[col] for col in ['asia_e', 'financial', 'money', 'edaily']]
    )

# 누적 총합 꺾은선 그래프 추가
ax2 = ax1.twinx()
ax2.plot(
    pivot.index, pivot['total'].cumsum(), 
    color=color_dict['line'], marker='o', linestyle='-', linewidth=2, markersize=8, label='누적 합계')

# 꺾은선이 확실히 위로 가도록 y축 설정
ax2.set_ylim(0, pivot['total'].cumsum().max() * 1.2)

# 제목 및 레이블 설정
# ax1.set_title('뉴스 언론사별 연별 누적 기사수 및 총합 누적 그래프', fontsize=16)
# ax1.set_xlabel('연도', fontsize=12)
# ax1.set_ylabel('기사수(연간)', fontsize=12)
# ax2.set_ylabel('누적 기사수', fontsize=12)

ax1.title.set_color('white')  # 제목 색상
ax1.xaxis.label.set_color('black')  # X축 라벨 색상
ax1.yaxis.label.set_color('black')  # Y축 라벨 색상
ax2.yaxis.label.set_color('black')  # 보조 Y축 라벨 색상

ax1.tick_params(colors='white')  # X축 & Y축 눈금 색상
ax2.tick_params(colors='white')  # 보조 Y축 눈금 색상

ax1.spines['bottom'].set_color('white')
ax1.spines['left'].set_color('white')
ax1.spines['top'].set_color('white')
ax1.spines['right'].set_color('white')

ax2.spines['bottom'].set_color('white')
ax2.spines['left'].set_color('white')
ax2.spines['top'].set_color('white')
ax2.spines['right'].set_color('white')

# 범례 설정
ax1.legend(loc='upper left', labelcolor='white')
ax2.legend(['누적 총합'], loc='upper right')

# 시각화 설정
plt.xticks(rotation=45, color='white')
plt.grid(axis='y', linestyle='--', alpha=0.5, color='white')
plt.tight_layout()

# 그래프 PNG 파일 저장
save_path = "C:/Users/hp/Downloads/news_graph/news_graph.png"  # 저장할 경로 지정 가능
plt.savefig(save_path, dpi=300, bbox_inches='tight')

# 그래프 출력
plt.show()