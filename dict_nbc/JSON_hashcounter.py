import json
from collections import Counter

# JSON 파일 로드
input_file = "D:/bok4_resource/json_dict/00final_dict/final_dict/final_dictionary_with_hash.json"
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 1. 모든 hash 값을 수집
hash_values = [value["hash"] for value in data.values()]

# 2. hash 값의 빈도 계산
hash_counts = Counter(hash_values)

# 3. 각 항목에 hashcount 추가
for key, value in data.items():
    value["hashcount"] = hash_counts[value["hash"]]

# 결과를 새 JSON 파일로 저장
output_file = input_file.replace(".json", "_with_hashcount.json")
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"해시 카운트가 추가된 데이터가 '{output_file}'에 저장되었습니다.")
