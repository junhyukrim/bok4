import os
import json

def remove_entries_with_count_one(folder_path):
    """
    폴더 내 모든 JSON 파일에서 count가 1인 항목을 삭제하고, 해당 파일에 바로 적용합니다.

    Args:
        folder_path (str): JSON 파일이 저장된 폴더 경로.
    """
    # 폴더 내 모든 JSON 파일 탐색
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):  # JSON 파일만 처리
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_name}")

            # JSON 파일 로드
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # count가 1인 항목 제거
            filtered_data = {key: value for key, value in data.items() if value.get('count', 0) > 1}

            # 수정된 데이터 저장 (원래 파일에 덮어쓰기)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(filtered_data, f, ensure_ascii=False, indent=4)

            print(f"Updated file: {file_name}")

# 실행 예제
if __name__ == "__main__":
    folder_path = "D:/download/머니투데이누락_scores"  # JSON 파일이 담긴 폴더 경로
    remove_entries_with_count_one(folder_path)
