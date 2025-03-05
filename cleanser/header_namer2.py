import os

def prepend_name_to_json_files(folder_path, prefix):
    """
    폴더 내 모든 JSON 파일의 이름 앞에 특정 이름을 붙입니다.
    
    Args:
        folder_path (str): JSON 파일들이 저장된 폴더 경로.
        prefix (str): 파일 이름 앞에 붙일 문자열.
    
    Returns:
        None
    """
    # 폴더 내 모든 파일 탐색
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):  # JSON 파일만 처리
            old_file_path = os.path.join(folder_path, file_name)
            
            # 새로운 파일 이름 생성
            new_file_name = f"{prefix}{file_name}"
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # 파일 이름 변경
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {file_name} -> {new_file_name}")

# 실행 예제
if __name__ == "__main__":
    folder_path = "D:/download/news_asiae_scores/dict_asiae"  # JSON 파일들이 있는 폴더 경로
    prefix = "news_ae_"  # 붙일 이름
    
    prepend_name_to_json_files(folder_path, prefix)
