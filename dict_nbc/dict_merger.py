import os
import json
from collections import defaultdict

def load_json_files(folder_path):
    """
    폴더 내 모든 JSON 파일을 읽어들입니다.
    
    Args:
        folder_path (str): JSON 파일이 저장된 폴더 경로.
    
    Returns:
        list: 각 JSON 파일의 데이터를 담은 리스트.
    """
    json_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):  # JSON 파일만 처리
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data.append(json.load(f))
    return json_data

def merge_and_filter_dictionaries(json_data_list, min_count=15):
    """
    여러 JSON 데이터를 병합하고 가중평균을 계산하며,
    count가 min_count 이상인 n-gram만 포함하는 최종 사전을 생성합니다.
    
    Args:
        json_data_list (list): 각 JSON 데이터 리스트.
        min_count (int): 포함할 최소 등장 횟수.
    
    Returns:
        dict: 최종 병합된 사전.
    """
    merged_dict = defaultdict(lambda: {'count': 0, 'score_sum': 0})

    # 각 JSON 데이터 병합
    for data in json_data_list:
        for ngram, values in data.items():
            merged_dict[ngram]['count'] += values['count']
            merged_dict[ngram]['score_sum'] += values['score'] * values['count']

    # 최종 평균 점수 계산 및 필터링
    final_dict = {}
    for ngram, values in merged_dict.items():
        if values['count'] >= min_count:  # 최소 등장 횟수 조건
            final_dict[ngram] = {
                'count': values['count'],
                'score': values['score_sum'] / values['count']
            }

    return final_dict

def save_to_json(data, output_folder, output_file_name="final_dictionary.json"):
    """
    데이터를 지정된 폴더에 JSON 파일로 저장합니다.
    
    Args:
        data (dict): 저장할 데이터.
        output_folder (str): 출력 폴더 경로.
        output_file_name (str): 출력 파일 이름.
    
    Returns:
        None
    """
    # 출력 폴더 생성
    os.makedirs(output_folder, exist_ok=True)
    
    # JSON 파일 저장
    output_path = os.path.join(output_folder, output_file_name)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Final dictionary saved to {output_path}")

# 메인 실행 함수
def main(input_folder, output_folder):
    print("Loading JSON files from folder...")
    json_data_list = load_json_files(input_folder)
    
    print("Merging dictionaries and filtering by count...")
    final_dict = merge_and_filter_dictionaries(json_data_list, min_count=15)
    
    print("Saving final dictionary to folder...")
    save_to_json(final_dict, output_folder)

# 실행 예제
if __name__ == "__main__":
    input_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/json_dict"  # JSON 파일이 담긴 폴더 경로
    output_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/json_dict/final_dict"  # 최종 사전 저장 폴더 경로
    
    main(input_folder, output_folder)
