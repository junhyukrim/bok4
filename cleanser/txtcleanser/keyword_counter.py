import os

def count_keywords_in_file(file_path, keywords):
    """
    파일에서 특정 키워드 리스트의 등장 횟수를 계산합니다.

    :param file_path: 텍스트 파일 경로
    :param keywords: 검색할 키워드 리스트
    :return: 각 키워드의 등장 횟수 합계
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 각 키워드의 등장 횟수 계산
    total_count = sum(content.count(keyword) for keyword in keywords)
    return total_count

def rename_files_in_folder(folder_path, keywords):
    """
    폴더 내 모든 .txt 파일에서 키워드 등장 횟수를 계산하고,
    해당 횟수를 파일명 앞에 붙여 파일명을 변경합니다.

    :param folder_path: 텍스트 파일들이 있는 폴더 경로
    :param keywords: 검색할 키워드 리스트
    """
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            old_file_path = os.path.join(folder_path, filename)
            
            # 키워드 등장 횟수 계산
            count = count_keywords_in_file(old_file_path, keywords)
            
            # 새로운 파일명 생성
            new_filename = f"{count}_{filename}"
            new_file_path = os.path.join(folder_path, new_filename)
            
            # 파일명 변경
            os.rename(old_file_path, new_file_path)

# 사용 예시
if __name__ == "__main__":
    folder_path = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/4_2토의내용X_perioded"  # 텍스트 파일들이 있는 폴더 경로
    keywords = ["의안 제", "보고 제"]  # 검색할 키워드 리스트

    rename_files_in_folder(folder_path, keywords)
