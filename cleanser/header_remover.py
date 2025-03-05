import os

def rename_txt_files(folder_path):
    """
    지정된 폴더 내 txt 파일의 이름에서 첫 번째 언더스코어(_) 이전 부분을 제거
    :param folder_path: txt 파일들이 있는 폴더 경로
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):  # .txt 파일만 처리
            # 첫 번째 언더스코어(_) 이후의 부분만 새로운 파일명으로 설정
            new_filename = filename.split("_", 1)[1] if "_" in filename else filename
            
            # 기존 파일 경로와 새로운 파일 경로 설정
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            
            # 파일 이름 변경
            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {filename} -> {new_filename}")

# 설정 값
folder_path = "D:/bok4_resource/json_dict/news_mt/final_dict"  # txt 파일이 있는 폴더 경로

# 실행
rename_txt_files(folder_path)
