import scrapy
import pandas as pd
import re
import os

class NewsSpider(scrapy.Spider):
    name = "news"
    custom_settings = {
        'JOBDIR': 'crawls/news_spider_state',
        # 'FEED': {} # Scrapy 기본 저장 방식 비활성화
    }

    # 합친 csv에서 url 목록 불러오기
    def start_requests(self):
        df = pd.read_csv('C:/Users/wosle/OneDrive/Desktop/Bok_Projet_woslek/Financial_News_text/news_scraper/news_scraper/spiders/filtered_matching_urls_2021_01_20_이후.csv')
        urls = df['url'].tolist()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # 웹에서 본문 크롤링
    def parse(self, response):
        title = response.css('h2#title_area span::text').get(default='N/A')
        date_raw = response.css('span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME::attr(data-date-time)').get(default="N/A")

        # 'article#dic_area' 안의 p, br, 그리고 다른 태그들을 포함한 HTML을 그대로 가져오기
        content_html = response.css('article#dic_area').get()

        # 가져온 HTML에서 <p>와 <br>을 포함한 내용을 정리해서 추출
        content = self.clean_html(content_html)

        if not content:
            content = ' '.join(response.css('div#contents.newsct_body::text').getall()).strip()

        # 로그에 date_raw 값 출력 (디버깅용)
        self.log(f"DEBUG: Extracted date_raw: {date_raw}")

        # 날짜에서 시간 제거
        if date_raw and date_raw != 'N/A':
            clean_date = date_raw.split(' ')[0]
        else:
            clean_date = 'unknown_date'

        # URL에서 고유 기사 ID 추출
        article_id_match = re.search(r'/(\d{10})\?', response.url)
        article_id = article_id_match.group(1) if article_id_match else "no_id"

        # 텍스트파일 저장할 폴더 생성 (없으면 자동 생성)
        save_path = "news_texts"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        # 파일명 만들기
        file_title = re.sub(r'[\\/*?:"<>|]', "_", clean_date)
        file_name = f'news_{file_title}_{article_id}.txt'

        with open(f'news_texts/{file_name}','w', encoding='utf-8') as f:
            f.write(f'{title}\n')
            f.write(f'{clean_date}\n')
            f.write(f'{content}\n')

        self.log(f'Saved file: {file_name}')

    # HTML에서 <p>와 <br>을 포함한 내용 정리
    def clean_html(self, html):
        # <p>와 <br> 태그를 기준으로 내용 추출
        content = re.sub(r'<br\s*/?>', '\n', html)  # <br> 태그를 줄바꿈으로 변환
        content = re.sub(r'<p\s*/?>', '\n', content)  # <p> 태그를 줄바꿈으로 변환
        content = re.sub(r'<[^>]+>', '', content)  # HTML 태그 제거
        return content.strip()

      # 스크래피 실행 시 터미널에 다음과 같은 명령어 입력: scrapy crawl news