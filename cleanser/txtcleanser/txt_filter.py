import os
import shutil

def sort_files_by_keyword(source_folder, a_folder, b_folder, keyword):
    # 대상 폴더가 없으면 생성
    for folder in [a_folder, b_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # 소스 폴더의 모든 파일을 순회
    for filename in os.listdir(source_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(source_folder, filename)
            
            # 파일 내용 읽기
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 키워드 검사 및 파일 이동
            if keyword in content:
                destination = os.path.join(a_folder, filename)
            else:
                destination = os.path.join(b_folder, filename)
            
            shutil.move(file_path, destination)

# 사용 예시
source_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/content_only"
a_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/content_only/토의결론O"
b_folder = "D:/download/txt_bok_min-20250307T015930Z-001/txt_bok_min/content_only/토의결론X"
keyword = ") 토의결론"

sort_files_by_keyword(source_folder, a_folder, b_folder, keyword)
