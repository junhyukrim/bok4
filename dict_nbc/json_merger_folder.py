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
            print(f"Loading file: {file_name}")  # 파일 로드 시작 메시지
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data.append(json.load(f))
            print(f"File loaded: {file_name}")  # 파일 로드 완료 메시지
    return json_data

def merge_and_filter_dictionaries(json_data_list, min_count=1):
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
    print("Merging dictionaries...")
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

    print("Dictionaries merged and filtered.")  # 병합 및 필터링 완료 메시지
    return final_dict

def save_to_json(data, output_folder, output_file_name):
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

def process_all_subfolders(parent_folder, output_folder):
    """
    부모 디렉토리 내 모든 하위 폴더를 처리하여 결과를 저장합니다.
    
    Args:
        parent_folder (str): 부모 디렉토리 경로.
        output_folder (str): 결과 저장 디렉토리 경로.
    
    Returns:
        None
    """
    for subfolder in os.listdir(parent_folder):
        subfolder_path = os.path.join(parent_folder, subfolder)
        
        if os.path.isdir(subfolder_path):  # 하위 폴더만 처리
            print(f"Processing folder: {subfolder}")
            
            # JSON 데이터 로드
            json_data_list = load_json_files(subfolder_path)
            
            # 병합 및 필터링 수행
            final_dict = merge_and_filter_dictionaries(json_data_list, min_count=15)
            
            # 결과 저장 (파일명에 하위 폴더명 포함)
            output_file_name = f"final_dictionary_{subfolder}.json"
            save_to_json(final_dict, output_folder, output_file_name)

# 실행 예제
if __name__ == "__main__":
    parent_folder = "D:/bok4_resource/json_dict/00final_dict"  # 상위 디렉토리 경로
    output_folder = "D:/bok4_resource/json_dict/00final_dict/final_dict"  # 결과 저장 디렉토리
    
    process_all_subfolders(parent_folder, output_folder)
