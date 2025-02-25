import os
import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict

# 저장 폴더 설정
download_folder = "naver_reports_pdf"
os.makedirs(download_folder, exist_ok=True)

# 파일명에서 특수 문자 제거하는 함수
def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)

# Selenium 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ChromeDriver 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 동일 날짜 & 동일 증권사 발행 개수 카운트
file_count = defaultdict(int)  # {"날짜_증권사": 개수}

# 최대 페이지 설정
max_pages = 281
downloaded_count = 0  # 다운로드된 파일 개수

# 페이지 순회하며 크롤링
for page in range(1, max_pages + 1):
    url = f"https://finance.naver.com/research/debenture_list.naver?page={page}"
    driver.get(url)
    time.sleep(2)  # 페이지 로드 대기

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # 테이블 행 가져오기
    rows = soup.select("table.type_1 tbody tr")

    for row in rows:
        columns = row.find_all("td")
        if len(columns) < 4:
            continue  # 데이터가 부족한 행 스킵

        title_tag = columns[0].find("a")  # 제목
        date_tag = row.find("td", class_="date")  # 날짜
        pdf_tag = columns[2].find("a")  # PDF 다운로드 링크

        # 증권사 정보 추출 (제목 다음 <td>에서 가져오기)
        issuer = columns[1].text.strip()  # 두 번째 <td>에서 증권사명 가져오기
        issuer = sanitize_filename(issuer)  # 특수 문자 제거

        if title_tag and date_tag and pdf_tag and issuer:
            title = title_tag.text.strip()  
            title = sanitize_filename(title)  # 특수 문자 제거
            date = date_tag.text.strip().replace(".", "")  # YYYYMMDD 형식
            pdf_link = urljoin("https://finance.naver.com", pdf_tag["href"])  # 절대 경로 변환

            # 동일 날짜 + 동일 증권사 PDF 개수 증가
            key = f"{date}_{issuer}"
            file_count[key] += 1
            count = file_count[key]  # 현재 개수 가져오기

            # 저장할 파일명 설정
            file_name = f"{date}_{issuer}_{count}.pdf"
            file_path = os.path.join(download_folder, file_name)

            # PDF 다운로드
            response = requests.get(pdf_link, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f" 다운로드 완료: {file_name}")
                downloaded_count += 1  # 다운로드 개수 증가
            else:
                print(f" 다운로드 실패: {pdf_link}")

    print(f"{page}/{max_pages} 페이지 완료")

# 브라우저 종료
driver.quit()
print(f"다운로드 완료! (총 {downloaded_count}개 저장, 폴더: {download_folder})")
