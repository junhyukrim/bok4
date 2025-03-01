import os

def clean_text_file(input_file_path, output_file_path):
    """
    텍스트 파일을 클렌징하여 지정된 규칙에 따라 내용을 수정하고 저장
    :param input_file_path: 원본 텍스트 파일 경로
    :param output_file_path: 클렌징된 텍스트 파일 저장 경로
    """
    with open(input_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    # 클렌징 규칙 적용
    cleaned_lines = []
    inside_exclusion_block = False  # 제외 블록 내부인지 확인하는 플래그

    for line in lines:
        # (cid:122) 삭제
        line = line.replace("(cid:122)", "").strip()

        # '채권시황' 또는 '채권 시황'으로 시작하는 줄 찾기
        if any(line.startswith(keyword) for keyword in ['채권시황', '채권 시황']):
            inside_exclusion_block = True  # 제외 블록 시작
            continue
        
        # '관심 차트 및 경제지표' 또는 '관심차트 및 경제지표'로 시작하는 줄 찾기
        if any(line.startswith(keyword) for keyword in ['관심 차트 및 경제지표', '관심차트 및 경제지표']):
            inside_exclusion_block = False  # 제외 블록 종료
            continue
        
        # 제외 블록 내부가 아니면 저장
        if inside_exclusion_block:
            cleaned_lines.append(line)

    # 결과 저장
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(cleaned_lines))
    print(f"Cleaned: {input_file_path} -> {output_file_path}")

def process_folder(input_folder, output_folder):
    """
    폴더 내 모든 텍스트 파일을 클렌징하여 새로운 폴더에 저장
    :param input_folder: 원본 텍스트 파일들이 있는 폴더 경로
    :param output_folder: 클렌징된 텍스트 파일을 저장할 폴더 경로
    """
    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 입력 폴더 내 모든 txt 파일 순회
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # .txt 파일만 처리
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            
            clean_text_file(input_file_path, output_file_path)

# 설정 값
input_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_txt/bond_txt/0_패턴분석완료_대우증권/output/daewoopattern"  # 원본 텍스트 파일 폴더 경로
output_folder = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_txt/bond_txt/0_패턴분석완료_대우증권/output/daewoopattern/daewoopattern_cleaned"  # 클렌징된 텍스트 파일 저장 폴더 경로

# 실행
process_folder(input_folder, output_folder)
