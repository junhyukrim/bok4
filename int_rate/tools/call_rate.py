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

try:
    # 콜금리(1일물) 데이터 조회
    df = api.get_statistic_search(
        통계표코드="817Y002",       # 통계표 코드 (콜금리)
        주기="D",                  # 데이터 주기 (일별)
        검색시작일자="20080101",    # 시작 날짜
        검색종료일자="20250223",    # 종료 날짜
        통계항목코드1="010101000"     # 항목 코드 (콜금리 1일물)
    )

    # 데이터 확인 및 저장
    if df is not None and not df.empty:
        output_csv_path = "call_rate_1day.csv"
        df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
        print(f"데이터가 성공적으로 저장되었습니다: {output_csv_path}")
    else:
        print("조회된 데이터가 없습니다. 기간 또는 통계항목코드를 확인하세요.")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")
