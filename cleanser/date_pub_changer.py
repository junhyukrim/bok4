import os

def rename_pdf_files(folder_path):
    """
    지정된 폴더 내 PDF 파일의 이름을 '날짜_발행사_넘버.pdf'에서 '발행사_날짜_넘버.pdf'로 변경
    :param folder_path: PDF 파일들이 있는 폴더 경로
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):  # .pdf 파일만 처리
            # 파일 이름을 분리 (예: '090921_IBK투자증권_1.pdf')
            parts = filename.split("_")
            
            if len(parts) == 3:  # '날짜_발행사_넘버' 형식인지 확인
                date = parts[0]        # 날짜 부분 (예: '090921')
                company = parts[1]     # 발행사 부분 (예: 'IBK투자증권')
                number = parts[2]      # 넘버 부분 (예: '1.pdf')

                # 새로운 파일명 생성 (예: 'IBK투자증권_090921_1.pdf')
                new_filename = f"{company}_{date}_{number}"
                
                # 파일 경로 변경
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)
                
                # 파일 이름 변경
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")

# 설정 값
folder_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_pdf/bond_reports_pdf-20250227T122256Z-003/bond_reports_pdf/0_대우증권_패턴분석완료/새 폴더"  # PDF 파일이 있는 폴더 경로

# 실행
rename_pdf_files(folder_path)
