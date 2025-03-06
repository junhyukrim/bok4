from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime, timedelta

# 1. 날짜 및 초기 설정
ds = "2008.10.08"  # 시작 날짜 (YYYY.MM.DD 형식)
duration = 7       # 기본 기간 (days)
min_duration = 0   # 최소 기간

# 오늘 날짜 계산
today = datetime.now().strftime("%Y.%m.%d")

# 날짜 형식 변환 함수
def add_days_to_date(date_str, days):
    date_obj = datetime.strptime(date_str, "%Y.%m.%d")
    new_date_obj = date_obj + timedelta(days=days)
    return new_date_obj.strftime("%Y.%m.%d")

while True:
    try:
        # 종료 조건: ds가 오늘 날짜를 초과하면 중단
        if datetime.strptime(ds, "%Y.%m.%d") > datetime.strptime(today, "%Y.%m.%d"):
            print("시작 날짜가 오늘 날짜를 초과했습니다. 크롤링을 종료합니다.")
            break

        # 2. 종료 날짜 계산
        de = add_days_to_date(ds, duration)

        # Selenium 설정
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        driver = webdriver.Chrome(options=options)
        url = f"https://search.naver.com/search.naver?where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds={ds}&de={de}&docid=&related=0&mynews=1&office_type=1&office_section_code=3&news_office_checked=2003&nso=so%3Ar%2Cp%3Afrom20081002to20081002&is_sug_officeid=0&office_category=0&service_area=0"
        driver.get(url)

        # 무한 스크롤 처리
        SCROLL_PAUSE_TIME = 2  # 스크롤 간 대기 시간

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(driver.page_source, "html.parser")
        articles = soup.select(".news_wrap")  # 기사 목록 선택자

        # 데이터 수집
        results = []
        for article in articles:
            try:
                url_tag = article.select_one("a.info[href^='https://n.news.naver.com']")
                if url_tag:
                    url = url_tag["href"]
                    date_tag = url_tag.find_previous_sibling("span", class_="info")
                    date = date_tag.text.strip() if date_tag else "날짜 없음"
                    results.append({"url": url, "date": date})
            except Exception as e:
                print(f"Error parsing article: {e}")

        # 결과 저장 (CSV 파일)
        output_filename = f"naver_news_{ds.replace('.', '')}_{de.replace('.', '')}_e_today.csv"
        with open(output_filename, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["url", "date"])
            writer.writeheader()
            writer.writerows(results)

        print(f"크롤링 완료! 총 수집된 기사: {len(results)}")
        print(f"결과가 저장되었습니다: {output_filename}")
        
        driver.quit()

        # 다음 실행을 위한 ds 업데이트 (de + 1)
        ds = add_days_to_date(de, 1)
        
    except Exception as e:
        print(f"오류 발생: {e}")
        
        # duration을 줄여서 재시도 (최소값은 min_duration)
        duration -= 1
        if duration < min_duration:
            print("최소 기간에 도달하여 크롤링을 중단합니다.")
            break
        
    finally:
        try:
            driver.quit()
        except:
            pass
