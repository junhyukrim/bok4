import pandas as pd
from glob import glob

file_names = glob('D:/bok4_resource/news_labeled/파이낸셜최종라벨compact/*.csv')
total = pd.DataFrame()

for file_name in file_names:
    temp = pd.read_csv(file_name, sep=',', encoding='utf-8')
    total = pd.concat([total, temp], ignore_index=True)
    
total.to_csv('D:/bok4_resource/news_labeled/파이낸셜최종라벨compact/total.csv', index=False)

print(f"총 {len(total)}개의 데이터가 저장되었습니다.")
