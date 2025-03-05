import json
from decimal import Decimal, getcontext

def generate_precise_hash(x, y):
    """
    x: 정수 값 (count)
    y: -1 이상 1 이하의 소수 값 (score)
    
    두 값을 조합해 고유한 해시 값을 생성하는 함수.
    """
    # Decimal 모듈로 정밀도 설정 (소수점 8자리)
    getcontext().prec = 10  # 계산 시 정밀도를 높이기 위해 여유를 둠
    y_decimal = Decimal(str(y))  # float -> Decimal 변환 (문자열로 변환해 정확도 유지)
    
    # y를 정수로 변환 (소수점 8자리까지 스케일링)
    scaled_y = int(y_decimal * Decimal(10**8))
    
    # 고유 해시 생성 (x와 scaled_y 조합)
    prime = 31  # 소수를 곱하여 충돌 가능성 감소
    hash_value = x * prime + scaled_y*37
    
    return hash_value

# JSON 파일 로드
input_file = "D:/bok4_resource/json_dict/00final_dict/final_dict/final_dictionary.json"
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 각 항목에 해시 값 추가
for key, value in data.items():
    count = value.get("count", 0)  # count 값 가져오기, 없으면 기본값 0
    score = value.get("score", 0.0)  # score 값 가져오기, 없으면 기본값 0.0
    value["hash"] = generate_precise_hash(count, score)  # 해시 값 추가

# 결과를 새 JSON 파일로 저장
output_file = input_file.replace(".json", "_with_hash.json")
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"해시 값이 추가된 데이터가 '{output_file}'에 저장되었습니다.")
