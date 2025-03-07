import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_converted.csv')

# 'date' 열을 datetime 형식으로 변환
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# 날짜를 인덱스로 설정
df.set_index('date', inplace=True)

# 날짜순으로 정렬
df.sort_index(inplace=True)

# 변환된 데이터프레임을 새로운 CSV 파일로 저장
output_csv_path = 'D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_converted.csv'
df.to_csv(output_csv_path, encoding='utf-8-sig')

print(f"변환된 데이터가 {output_csv_path}에 저장되었습니다.")