import json
import os  # 파일 경로 처리를 위해 os 모듈 사용

# 원본 JSON 파일 경로
input_file = 'D:/bok4_resource/json_dict/00final_dict/final_dict/final_dictionary_100filtered_sorted.json'

# JSON 파일 로드
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 사용자 지정 필터링 조건
a = -0.2  # score가 a보다 작다
b = 0.2   # score가 b보다 크다

# 1. count가 50 이상이고, score 조건을 만족하는 항목 필터링
filtered_data = {
    key: value for key, value in data.items()
    if value['count'] >= 100 and (value['score'] < a or value['score'] > b)
}

# 2. score 기준으로 내림차순 정렬
sorted_data = dict(sorted(filtered_data.items(), key=lambda x: x[1]['score'], reverse=True))

# 원본 파일명에서 디렉터리와 확장자 분리
file_dir, file_name = os.path.split(input_file)
file_base, file_ext = os.path.splitext(file_name)

# 새로운 파일명 생성 (원본 파일명 + '_filtered_sorted')
output_file = os.path.join(file_dir, f"{file_base}_neutral_removed{file_ext}")

# 결과를 새 파일로 저장
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(sorted_data, file, ensure_ascii=False, indent=4)

print(f"필터링 및 정렬된 데이터가 '{output_file}'에 저장되었습니다.")
