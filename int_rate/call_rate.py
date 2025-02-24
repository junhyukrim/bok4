from PublicDataReader import Ecos

# ECOS API 인증키 (한국은행 Open API에서 발급받아야 함)
service_key = ""

# ECOS 객체 생성
api = Ecos(service_key)

# 콜금리 데이터 조회 (통계표코드: 722Y001, 항목코드: 0101000)
df = api.get_statistic_search(
    통계표코드="722Y001",       # 통계표 코드 (시장금리)
    주기="D",                  # 데이터 주기 (D: 일별, M: 월별 등)
    검색시작일자="20080101",    # 시작 날짜
    검색종료일자="20250223",    # 종료 날짜
    통계항목코드1="0101000"     # 항목 코드 (콜금리 익일물)
)

# 데이터 출력
print(df)
