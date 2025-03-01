import os

def clean_text_file(file_path, keywords):
    """
    텍스트 파일에서 특정 키워드 이후의 모든 텍스트를 삭제하고 원본에 직접 반영
    :param file_path: 텍스트 파일 경로
    :param keywords: 키워드 리스트 (예: ['그림 1.', '그림 2.'])
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # 특정 키워드 이후의 모든 텍스트 삭제
    for keyword in keywords:
        if keyword in content:
            content = content.split(keyword)[0]
            break  # 첫 번째 키워드만 처리하고 종료

    # 원본 파일에 덮어쓰기
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Cleaned: {file_path}")

def process_folder(folder_path, keywords):
    """
    폴더 내 모든 텍스트 파일을 처리하여 특정 키워드 이후의 텍스트를 삭제
    :param folder_path: 텍스트 파일들이 있는 폴더 경로
    :param keywords: 키워드 리스트 (예: ['그림 1.', '그림 2.'])
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # .txt 파일만 처리
            file_path = os.path.join(folder_path, filename)
            clean_text_file(file_path, keywords)

# 설정 값
folder_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/1_현대차증권/center_bond_plus/txted"  # 텍스트 파일 폴더 경로
keywords = ['<그림','■','관심 차트 및 경제지표', '예상 금리 레인지','(그림1)','▶ Check Point','▶ Bond Market Check Point','주간 레인지 전망','월간 레인지 전망', '그림 1.', '그림 2.','표 1.','Key Charts','향후 국고채 3년','금리와 신용스프레드','국채 금리와 외국인 국채선물 누적순매수','실적 패턴을 이용한 최종 선택 그룹','국내주요금리 (%,']  # 삭제 기준이 되는 키워드 리스트

# 실행
process_folder(folder_path, keywords)
