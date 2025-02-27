from pathlib import Path
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
        df = pd.read_csv('C:/Users/egege/OneDrive/Documents/bok4_resource/news_url_csv/money_today/total.csv')
        urls = df['url'].tolist()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # 웹에서 본문 크롤링
    def parse(self, response):
        title = response.css('h2#title_area span::text').get(default='N/A')
        date_raw = response.css('span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME::attr(data-date-time)').get(default="N/A")
        content = ' '.join(response.css('div.newsct_article p::text').getall()).strip()

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

        # 스크래피 실행 시 터미널에 다음과 같은 명령어 입력: `scrapy crawl news`

