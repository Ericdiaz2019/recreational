import scrapy
from scrapy_playwright.page import PageMethod
from bs4 import BeautifulSoup
import re
import csv
import math
import datetime
import time

today = datetime.date.today()


class generalrv(scrapy.Spider):
    name = "generalrv"


    def start_requests(self):
        web_links = {
            'Travel Trailer': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=29&pagesize=12',
            'FifthWheel': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=5&pagesize=12',
            'ToyHauler': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=26%2C28&pagesize=12',
            'ClassC Gas': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=16&pagesize=12',
            'ClassC Diesel': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=17&pagesize=12',
            'ClassC ToyHauler': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=19&pagesize=12',
            'ClassC Super Diesel': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=95&pagesize=12',
            'ClassB Gas': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=13&pagesize=12',
            'ClassB Diesel': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=116&pagesize=12',
            'ClassB Gas+': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=14&pagesize=12',
            'ClassA Gas': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=9&pagesize=12',
            'ClassA Diesel': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=10&pagesize=12',
            'ClassA Diesel ToyHauler': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=11&pagesize=12',
            'ClassA Gas ToyHauler': 'https://www.generalrv.com/rv-search?s=true&condition=1&types=12&pagesize=12',
            'Destination Trailer' : 'https://www.generalrv.com/rv-search?s=true&condition=1&types=3&pagesize=12'
        }

        for category_name, link_url in web_links.items():
            yield scrapy.Request(
                url=link_url,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", "span.total-units"),
                    ],
                    'playwright_context': 'default',  # Use default browser context
                    'category_name': category_name
                },
                callback=self.parse
            )

    def parse(self, response):
        self.logger.info(f"Processing category {response.meta['category_name']}")

        page_content = response.text
        soup = BeautifulSoup(page_content, 'lxml')

        count = soup.find('span', class_='total-units').text
        amount = math.ceil(int(count) / 12)

        for i in range(1, amount + 1):
            page_url = f'{response.url}&page={i}'

            # Adding retries and a longer timeout for each page load
            yield scrapy.Request(
                url=page_url,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", "li.standard-template-v2"),
                    ],
                    'playwright_context': 'default',  # Use default browser context
                    'category_name': response.meta['category_name']
                },
                callback=self.parse_units,
                errback=self.handle_error,  # Error handling in case of failure
                dont_filter=True
            )

        
    
    def parse_units(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        units = soup.find_all('li', class_='standard-template-v2')

        for unit in units:
            unit_year = unit.find('span', class_='unit-year').text
            unit_company = unit.find('span', class_='unit-mfg').text
            unit_brand = unit.find('span', class_='unit-brand').text
            unit_floor = unit.find('span', class_='unit-model').text
            unit_stock = unit.find('span', class_='stock-number-text').text
            unit_location = unit.find('span', class_='unit-location-text').text.replace('.','').replace(',','').replace('""','').strip()
            unit_category = response.meta['category_name']
            try:
                unit_msrp = unit.find('span', class_='regPriceText').text.replace('$','').replace(',','').strip()
            except:
                unit_msrp = 'N/A'
            
            try:
                unit_discount = unit.find('span', class_='salePriceText').text.replace('$','').replace(',','').strip()
            except:
                unit_discount = 'N/A'

            with open(f'DailyFiles/GeneralRV {today}.csv', 'a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                if file.tell() == 0:  # If file is empty, write header
                    writer.writerow(['Year','Company','Brand','FloorPlan','Msrp','Discount','Stock-Number','Unit Type','Location','Dealer','Date'])
                
                writer.writerow([unit_year,unit_company,unit_brand,unit_floor,unit_msrp,unit_discount,unit_stock,unit_category,unit_location,'GeneralRV',today])

    def handle_error(self, failure):
        self.logger.error(repr(failure))
        self.logger.info('Retrying request...')

