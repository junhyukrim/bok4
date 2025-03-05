import os

def add_prefix_to_filenames(folder_path, prefix):
    try:
        for file_name in os.listdir(folder_path):
            old_path = os.path.join(folder_path, file_name)
            if os.path.isfile(old_path):
                new_name = prefix + file_name
                new_path = os.path.join(folder_path, new_name)
                os.rename(old_path, new_path)
        print("모든 파일 이름에 접두사가 성공적으로 추가되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

# 사용 예시
folder_path = "D:/download/이데일리_jason/이데일리_jason"  # 실제 폴더 경로로 변경하세요
prefix = "news_EDIALY_"  # 원하는 접두사로 변경하세요
add_prefix_to_filenames(folder_path, prefix)
