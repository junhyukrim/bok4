from PublicDataReader import Ecos
import requests

service_key = "AAO7WPKGFANGOX1RNAID"
api = Ecos(service_key)

response = api.get_statistic_search(
    통계표코드="817Y002",
    주기="D",
    검색시작일자="20250109",
    검색종료일자="20250306",
    통계항목코드1="010101000"
)

print(api.url)