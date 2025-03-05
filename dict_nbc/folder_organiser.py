import os
import math
import shutil

def split_files_into_folders(source_folder, n):
    """
    파일을 n개씩 나누어 새로운 폴더(p1, p2, ...)로 분류합니다.
    
    Args:
        source_folder (str): 원본 파일들이 저장된 폴더 경로.
        n (int): 각 폴더에 포함될 파일의 개수.
    
    Returns:
        None
    """
    # 원본 폴더에서 모든 파일 가져오기
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    
    # 파일 이름 정렬 (필요시 사용자 정의 정렬 기준 적용 가능)
    files.sort()
    
    # 총 필요한 폴더 수 계산
    total_files = len(files)
    num_folders = math.ceil(total_files / n)
    
    print(f"Total files: {total_files}")
    print(f"Number of folders to create: {num_folders}")
    
    # 각 폴더 생성 및 파일 이동
    for i in range(num_folders):
        folder_name = f"p{i+1}"  # 폴더 이름: p1, p2, ...
        folder_path = os.path.join(source_folder, folder_name)
        
        # 폴더 생성
        os.makedirs(folder_path, exist_ok=True)
        
        # 현재 폴더에 포함될 파일 인덱스 계산
        start_idx = i * n
        end_idx = min(start_idx + n, total_files)
        current_files = files[start_idx:end_idx]
        
        print(f"Creating folder: {folder_name} with {len(current_files)} files.")
        
        # 파일 이동
        for file_name in current_files:
            src_file_path = os.path.join(source_folder, file_name)
            dest_file_path = os.path.join(folder_path, file_name)
            shutil.move(src_file_path, dest_file_path)
    
    print("File distribution completed.")

# 실행 예제
if __name__ == "__main__":
    source_folder = "D:/bok4_resource/json_dict/news_mt"  # 원본 파일들이 있는 디렉토리 경로
    n = 10  # 각 폴더에 포함할 파일 개수
    
    split_files_into_folders(source_folder, n)
