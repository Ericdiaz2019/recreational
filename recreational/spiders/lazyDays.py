import scrapy
from scrapy_playwright.page import PageMethod
from bs4 import BeautifulSoup
import re
import csv
import math
import datetime
import time

today = datetime.date.today()


class lazydays(scrapy.Spider):
    name = "lazydays"

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'RETRY_TIMES': 5,  # Retry up to 5 times
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': 120000,
    }


    def start_requests(self):
        web_links = {
            'Travel Trailer': 'https://www.lazydays.com/rvs/travel-trailer-rvs?new=true&pageSize=4000',
            'FifthWheel': 'https://www.lazydays.com/rvs/fifth-wheel-rvs?new=true&pageSize=2000',
            'ToyHauler': 'https://www.lazydays.com/rvs/toy-hauler-rvs?new=true&pageSize=1000',
            'ClassC Gas': 'https://www.lazydays.com/rvs/class-c-motorhomes?new=true&fuel=G&pageSize=1800',
            'ClassC Diesel': 'https://www.lazydays.com/rvs/class-c-motorhomes?new=true&fuel=D&pageSize=1800',
            'ClassB Gas': 'https://www.lazydays.com/rvs/class-c-motorhomes?new=true&classes=B&fuel=G&pageSize=1800',
            'ClassB Diesel': 'https://www.lazydays.com/rvs/class-c-motorhomes?new=true&classes=B&fuel=D&pageSize=1800',
            'ClassA Gas': 'https://www.lazydays.com/rvs?new=true&classes=AG&fuel=G&pageSize=1800',
            'ClassA Diesel': 'https://www.lazydays.com/rvs/class-a-diesel-motorhomes?new=true&pageSize=1000'
        }

        for category_name, link_url in web_links.items():
            yield scrapy.Request(
                url=link_url,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", "div.list-view"),
                    ],
                    'playwright_context': 'default',  # Use default browser context
                    'category_name': category_name,
                    'page_goto_timeout': 120000  # Increase timeout to 120 seconds (120000ms)

                },
                callback=self.parse
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        unit_div = soup.find_all('article', class_='post')

        for unit in unit_div:
            unit_year = unit.find('span','year').text.strip()
            unit_company = unit.find('span','make').text.strip()
            unit_brand = unit.find('span','model').text.strip()
            unit_floor = unit.find('span','floorplan').text.strip()
            unit_category = response.meta['category_name']
            try:
                unit_msrp = unit.find('li',class_='msrp').find_all('span')[1].text.replace('†', '').replace('$','').replace('Request Price','').replace(',','').strip()
            except:
                unit_msrp = 'N/A'

            try:
                unit_discount = unit.find('li',class_='saleprice').find_all('span')[1].text.replace('†', '').replace('$','').replace('Request Price','').replace(',','').strip()
            except:
                unit_discount = 'N/A'

            unit_location = unit.find('div', class_='location').find_all('span')[1].text.replace(',','')
            unit_stock = unit.find('div', class_='stocknumber').find('span').text.replace('Stock #: ','').replace('"','').strip()



            with open(f'DailyFiles/LazyDays {today}.csv', 'a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                if file.tell() == 0:  # If file is empty, write header
                    writer.writerow(['Year','Company','Brand','FloorPlan','Msrp','Discount','Stock-Number','Unit Type','Location','Dealer','Date'])
                
                writer.writerow([unit_year,unit_company,unit_brand,unit_floor,unit_msrp,unit_discount,unit_stock,unit_category,unit_location,'LazyDays',today])


    def handle_error(self, failure):
        self.logger.error(repr(failure))
        self.logger.info('Retrying request...')

