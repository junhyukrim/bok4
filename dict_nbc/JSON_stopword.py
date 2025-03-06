import json

# JSON 파일 경로
input_file = 'D:/bok4_resource/json_dict/00final_dict/final_dict_new/final_dictionary_last_neutral_removed.json'

# 삭제할 키워드 리스트
keywords_to_remove = ["이데일리", "네이버", "청춘/NNG 우스/NNG","꿀/NNG 잼/NNG","웹툰/NNG", "뉴스", "우스", "갤럭시", "워치", "비밀",
                      "애널리스트","박현준","리서치센터","공기청정기","암호화폐/NNG 시황/NNG","시황/NNG 사이트/NNG","취/NNP 준/NNP","알짜/NNG 정보/NNG","준/NNP 알짜/NNG"]  # 예시 키워드 리스트

# JSON 파일 로드
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 키워드가 포함된 항목 삭제
filtered_data = {
    key: value for key, value in data.items()
    if not any(keyword in key for keyword in keywords_to_remove)
}

# 결과를 새 JSON 파일로 저장
output_file = input_file.replace(".json", "_keywords_removed.json")
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=4)

print(f"키워드가 제거된 데이터가 '{output_file}'에 저장되었습니다.")
