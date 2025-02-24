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

# 저장 폴더 설정
download_folder = "naver_reports_pdf"
os.makedirs(download_folder, exist_ok=True)  # 폴더가 없으면 생성

# Windows에서 허용되지 않는 문자 제거 함수
def sanitize_filename(filename):
    return re.sub(r'[\/:*?"<>|]', '', filename)  # Windows에서 허용되지 않는 문자 제거

# Selenium 옵션 설정 (백그라운드 실행)
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ChromeDriver 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 최대 페이지 설정
max_pages = 281  # 전체 페이지 크롤링

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
        if len(columns) < 5:
            continue  # 데이터가 부족한 행 스킵

        title_tag = columns[0].find("a")  # 제목
        date_tag = row.find("td", class_="date")  # 날짜
        pdf_tag = columns[2].find("a")  # PDF 다운로드 링크 (3번째 열)

        if title_tag and date_tag and pdf_tag:
            title = title_tag.text.strip()  
            title = sanitize_filename(title)  # 특수 문자 제거
            date = date_tag.text.strip().replace(".", "")  # YYYYMMDD 형식
            pdf_link = urljoin("https://finance.naver.com", pdf_tag["href"])  # 절대 경로 변환

            # 저장할 파일명 설정
            file_name = f"{date}_{title}.pdf"
            file_path = os.path.join(download_folder, file_name)

            # PDF 다운로드
            response = requests.get(pdf_link, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f" 다운로드 완료: {file_name}")
            else:
                print(f" 다운로드 실패: {pdf_link}")

    print(f"{page}/{max_pages} 페이지 완료")

# 브라우저 종료
driver.quit()

print(f"모든 PDF 다운로드 완료! (저장 폴더: {download_folder})")