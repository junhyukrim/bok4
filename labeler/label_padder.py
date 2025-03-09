import pandas as pd

# CSV 파일 로드
data = pd.read_csv("D:/bok4_resource/bok_minute/minute_final.csv")

# 새로운 열 추가
data['train_test_label'] = 'test'

# CSV 파일 저장
data.to_csv("D:/bok4_resource/analysis/all_analysis_compact_bydate_eval_copy2_for_minute_test.csv", index=False)
