import pandas as pd
from glob import glob

file_names = glob('C:/Users/hp/Desktop/Bootcamp/bok4/csv_files/*.csv')
total = pd.DataFrame()

for file_name in file_names:
    temp = pd.read_csv(file_name, sep=',', encoding='utf-8')
    total = pd.concat([total, temp], ignore_index=True)
    
total.to_csv('C:/Users/hp/Desktop/Bootcamp/bok4/total.csv', index=False)

print(f"총 {len(total)}개의 데이터가 저장되었습니다.")