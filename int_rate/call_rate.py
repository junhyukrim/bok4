from PublicDataReader import Ecos
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv("config.env")

# API 키 가져오기
api_key = os.getenv("API_KEY")

# ECOS API 인증키 설정
service_key = api_key

# ECOS 객체 생성
api = Ecos(service_key)

# 콜금리 데이터 조회 
df = api.get_statistic_search(
    통계표코드="817Y002",       # 통계표 코드 (콜금리)
    주기="D",                  # 데이터 주기 (일별)
    검색시작일자="20250109",    # 시작 날짜
    검색종료일자="20250122",    # 종료 날짜
    통계항목코드1="010101000"     # 항목 코드 (콜금리 1일물)
)

print(df)

output_csv_path = "call_rate_data.csv"  # 저장할 파일 이름과 경로
df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')  # UTF-8 인코딩