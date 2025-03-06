import json
import math
import os

def split_large_json(input_file, output_folder, num_files):
    # 큰 JSON 파일 로드
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 파일당 항목 수 계산
    total_items = len(data)
    items_per_file = math.ceil(total_items / num_files)

    # 데이터를 작은 청크로 분할
    items = list(data.items())
    for i in range(num_files):
        start_index = i * items_per_file
        end_index = min((i + 1) * items_per_file, total_items)
        chunk = dict(items[start_index:end_index])

        # 각 청크를 별도의 JSON 파일로 저장
        output_file = os.path.join(output_folder, f"split_part_{i + 1}.json")
        with open(output_file, 'w', encoding='utf-8') as out_f:
            json.dump(chunk, out_f, ensure_ascii=False, indent=4)

    print(f"{num_files}개의 파일로 성공적으로 분할되었습니다.")

# 사용 예시
input_file = "large_file.json"  # 큰 JSON 파일 경로
output_folder = "output_folder"  # 분할된 파일을 저장할 폴더
num_files = 5  # 생성할 작은 파일의 수

# 출력 폴더가 존재하는지 확인
os.makedirs(output_folder, exist_ok=True)

split_large_json(input_file, output_folder, num_files)
