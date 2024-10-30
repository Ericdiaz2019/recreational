import scrapy
from scrapy_playwright.page import PageMethod
from bs4 import BeautifulSoup
import math
import urllib.parse
import datetime
import csv
import re
import os

today = datetime.date.today()

boat_naming = {
    'Barletta Boats': 'Barletta',
    '21 RL': '21RL',
    '21 RL Sport': '21RL-Sport',
    '21 L': '21L',
    '23 WRL': '23WRL',
    '23 RL Sport': '23RL-Sport',
    '210 CS': '210CS',
    '230 Sport': '230-Sport',
    '23 XT': '23XT',
}

def clean_boat_name(title_tag):
    boat_info = title_tag.strip()
    for old_name, new_name in boat_naming.items():
        if old_name in boat_info:
            boat_info = boat_info.replace(old_name, new_name)
    return boat_info

class powerLodge(scrapy.Spider):
    name = 'powerLodge'

    def start_requests(self):
        urls = {
            'Pontoon': 'https://www.powerlodgeramsey.com/search/inventory/availability/In%20Stock/sort/discount/type/Pontoons/type/Boats/usage/New/page/1',
        }

        for category_name, url in urls.items():
            yield scrapy.Request(
                url=url,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", "span.Units"),
                    ],
                    'playwright_context': 'default',
                    'category_name': category_name
                },
                callback=self.parse
            )

    def parse(self, response):
        self.logger.info(f"Processing category {response.meta['category_name']}")

        page_content = response.text
        soup = BeautifulSoup(page_content, 'lxml')

        label_total = soup.find('label', class_='search-results-count').text
        total_amount = re.search(r'of (\d+)', label_total).group(1)
        pages_qty = math.ceil(int(total_amount) / 30)

        self.logger.info(f'Total Pages To Scrape: {pages_qty}')

        for i in range(1, pages_qty + 1):
            page_url = f"{response.url.rsplit('/page/', 1)[0]}/page/{i}"
            self.logger.info(f"Fetching page {i} for category {response.meta['category_name']} - {page_url}")

            yield scrapy.Request(
                url=page_url,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", "span.Units"),
                    ],
                    'category_name': response.meta['category_name']
                },
                callback=self.parse_units,
                dont_filter=True
            )

    def parse_units(self, response):
        self.logger.info(f"Processing units for page: {response.url}")
        soup = BeautifulSoup(response.text, 'lxml')
        units = soup.find_all('div', class_='search-results-list')

        for boat in units:
            boat_year = boat.find('span', {'data-model-year' : ''}).text.strip
            print(boat_year)

            with open(f'DailyFiles/Power Lodge {today}.csv', 'a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                if file.tell() == 0:
                    writer.writerow(['Year', 'Company', 'Model', 'FloorPlan', 'Length', 'Engine', 'Stock Number', 'Dealer', 'Location', 'MSRP', 'DISCOUNT', 'Date'])
                
                #writer.writerow([boat_year, boat_company, boat_model, boat_floor, boat_length, boat_engine, boat_stock, 'Valley Marine', boat_location, boat_msrp, boat_discount, today])

    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
