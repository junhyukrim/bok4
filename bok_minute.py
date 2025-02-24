import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 다운로드 폴더 설정 (절대경로)
download_dir = r'C:\Users\hp\Desktop\Bootcamp\pdf_to_gdrive'

# Chrome 옵션 설정 (다운로드 폴더 지정)
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for page in range(5, 36):
    url = f'https://www.bok.or.kr/portal/singl/newsData/list.do?pageIndex={page}&targetDepth=3&menuNo=201154&syncMenuChekKey=14&depthSubMain=&subMainAt=&searchCnd=1&searchKwd=%EA%B8%88%EC%9C%B5%ED%86%B5%ED%99%94%EC%9C%84%EC%9B%90%ED%9A%8C%20%EC%9D%98%EC%82%AC%EB%A1%9D&depth2=200038&depth3=201154&date=5&sdate=2008-01-01&edate=2025-02-24&sort=1&pageUnit=100'
    driver.get(url)
    time.sleep(1)  # 페이지 로딩 대기

    # 리스트 페이지에서 상세 페이지 URL과 subject 미리 추출
    detail_pages = []
    li_elements = driver.find_elements(By.CSS_SELECTOR, '.bd-line li')
    for li in li_elements:
        try:
            link_elem = li.find_element(By.CSS_SELECTOR, '.set > a')
            detail_url = link_elem.get_attribute("href")
            subject = link_elem.text  # 제목 추출
            detail_pages.append((detail_url, subject))
        except Exception as e:
            print("링크 추출 오류:", e)

    # 추출한 상세 페이지들을 순회하면서 PDF 다운로드 및 파일명 변경 처리
    for detail_url, subject in detail_pages:
        try:
            # 다운로드 전 폴더 상태 기록
            files_before = set(os.listdir(download_dir))
            
            # 상세 페이지로 이동
            driver.get(detail_url)
            time.sleep(0.5)
            
            # PDF 다운로드 버튼을 위해 hover 동작 수행
            hover_element = driver.find_element(By.CSS_SELECTOR, '.down-button > button > span')
            hover_element.click()
            
            # 여러 다운로드 링크 중 PDF 링크 선택
            download_links = driver.find_elements(By.CSS_SELECTOR, '.down dd > ul li > div.file-set > a')
            pdf_link = None
            for link_elem in download_links:
                href = link_elem.get_attribute("href")
                if href and ".pdf" in href.lower():
                    pdf_link = link_elem
                    break

            if pdf_link:
                pdf_link.click()
            else:
                print("PDF 파일이 발견되지 않았습니다. (subject:", subject,")")
                continue

            # 파일 다운로드 완료까지 대기 (최대 30초)
            timeout = 30
            elapsed = 0
            new_file = None
            while elapsed < timeout:
                time.sleep(1)
                elapsed += 1
                files_after = set(os.listdir(download_dir))
                new_files = files_after - files_before
                if new_files:
                    new_file = new_files.pop()
                    break

            if new_file:
                # 확장자 추출 및 subject로 파일명 변경 (필요시 특수문자 처리)
                ext = os.path.splitext(new_file)[1]
                new_name = subject + ext
                old_path = os.path.join(download_dir, new_file)
                new_path = os.path.join(download_dir, new_name)
                os.rename(old_path, new_path)
                print(f"파일명 변경 완료: {new_name}")
            else:
                print("새 파일 감지 실패 (subject:", subject,")")
        except Exception as e:
            print("오류 발생:", e)
            
driver.quit()