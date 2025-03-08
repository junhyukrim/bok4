import os
import requests

# # API 키 가져오기
# api_key = os.getenv("API_KEY")

# # ECOS API 인증키 설정
# service_key = api_key


url = "https://ecos.bok.or.kr/api/StatisticSearch/AAO7WPKGFANGOX1RNAID/json/kr/1/10/817Y002/D/20250109/20250306/010101000"
response = requests.get(url)

if response.status_code == 200:
    print(response.json())  # JSON 응답 출력
else:
    print(f"Error: {response.status_code}, {response.text}")
