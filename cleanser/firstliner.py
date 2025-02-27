import os

def collect_first_lines(input_folder, output_file):
    """
    입력 폴더의 모든 텍스트 파일에서 첫 번째 줄을 읽어 
    출력 파일에 저장하는 함수
    
    Args:
        input_folder (str): 텍스트 파일이 있는 폴더 경로
        output_file (str): 결과를 저장할 파일 경로
    """
    # 출력 파일 열기
    with open(output_file, 'w', encoding='utf-8') as out_f:
        # 입력 폴더의 모든 파일 순회
        for filename in os.listdir(input_folder):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_folder, filename)
                
                # 파일이 실제로 파일인지 확인
                if os.path.isfile(file_path):
                    try:
                        # 파일 열고 첫 번째 줄 읽기
                        with open(file_path, 'r', encoding='utf-8') as f:
                            first_line = f.readline().strip()
                            
                            # 파일명과 함께 첫 번째 줄 저장
                            out_f.write(f"{filename}: {first_line}\n")
                    except Exception as e:
                        print(f"파일 {filename} 처리 중 오류 발생: {e}")

# 사용 예시
input_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_txt/bond_txt/test/input"  # 텍스트 파일이 있는 폴더 경로
output_file = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_txt/bond_txt/test/output/first_lines.txt"  # 결과를 저장할 파일 경로

collect_first_lines(input_folder, output_file)
print(f"모든 텍스트 파일의 첫 줄이 {output_file}에 저장되었습니다.")
