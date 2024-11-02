import scrapy
from scrapy_playwright.page import PageMethod
from bs4 import BeautifulSoup
import math
import urllib.parse
import datetime
import csv
import re

today = datetime.date.today()

boat_naming = {
    'Barletta Boats' : 'Barletta',
    '21 RL' : '21RL',
    '21 RL Sport' : '21RL-Sport',
    '21 L' : '21L',
    '23 WRL' : '23WRL',
    '23 RL Sport' : '23RL-Sport',
    '210 CS' : '210CS',
    '230 Sport' : '230-Sport',
    '23 XT' : '23XT',
}


def clean_boat_name(title_tag):
    # Extract and clean the boat name from the title_tag
    boat_info = title_tag.strip()
    
    # Iterate over the boat_naming dictionary to replace the naming conventions
    for old_name, new_name in boat_naming.items():
        if old_name in boat_info:
            boat_info = boat_info.replace(old_name, new_name)
    
    return boat_info

class andersonPower(scrapy.Spider):
    name = 'andersonPower'  # Unique identifier for the spider

    def start_requests(self):
        # Dictionary of URLs the spider will start with
        urls = { 
            'Pontoon': 'https://www.andersonpowersportsaz.com/default.asp?category=boat&condition=new&page=inventory&pg=1',  # Add more URLs as needed
        }

        for category_name, url in urls.items():
            yield scrapy.Request(
                url=url,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", "div.v7list-subheader__result-text"),
                    ],
                    'playwright_context': 'default',  # Use default browser context
                    'category_name': category_name  # Pass category name for logging
                },
                callback=self.parse
            )

    def parse(self, response):
        self.logger.info(f"Processing category {response.meta['category_name']}")

        # Use BeautifulSoup to parse the response
        page_content = response.text
        soup = BeautifulSoup(page_content, 'lxml')


        div_total = soup.find('div', class_='v7list-subheader__result-text')
        # Find all span elements within that div
        spans = div_total.find_all('span')
        # Extract the text from the second span (index 1 as indexing starts from 0)
        if len(spans) > 1:  # Ensure there are at least 2 spans
            total_amount = spans[1].text
            print(total_amount)  # This will output '4' based on the example HTML
        else:
            print("Not enough spans found")
                # Find the div with class 'result-status'

        # Calculate the number of pages (assuming 100 items per page)
        pages_qty = math.ceil(int(total_amount) / 20)
        
        self.logger.info(f'Total Pages To Scrape: {pages_qty}')

        # Parse the URL and query parameters
        parsed_url = urllib.parse.urlparse(response.url)
        query_params = dict(urllib.parse.parse_qsl(parsed_url.query))

        # Loop through all pages and update the 'p' (page) query parameter
        for i in range(1, pages_qty + 1):
            query_params['pg'] = i  # Update the 'p' (page) query parameter
            new_query_string = urllib.parse.urlencode(query_params)
            page_url = urllib.parse.urlunparse(
                parsed_url._replace(query=new_query_string)
            )

            self.logger.info(f"Fetching page {i} for category {response.meta['category_name']} - {page_url}")
            
            yield scrapy.Request(
                url=page_url,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", "div.v7list-subheader__result-text"),
                    ],
                    'category_name': response.meta['category_name']
                },
                callback=self.parse_units,
                dont_filter=True
            )

    def parse_units(self, response):
        # This is where you can parse the data from each page
        self.logger.info(f"Processing units for page: {response.url}")
        soup = BeautifulSoup(response.text, 'lxml')
        units = soup.find_all('li', class_='v7list-results__item')



        for boats in units:
            boat_year = boats.get('data-unit-year')
            boat_company = boats.get('data-unit-make').replace('®','').replace('™','')
            model_raw = boats.get('data-unit-model').replace('®','').replace('™','')
            split_model = model_raw.split()
            try:
                boat_location = boats.find('span', class_='v7list-vehicle__location-value').text.strip()
            except:
                boat_location = 'Parker AZ'
            if(len(split_model) > 1):
                boat_model = split_model[0]
                boat_floor = split_model[1]
            else:
                boat_model = 'N/A'
                boat_floor = split_model[0]


            try:
                boat_msrp = boats.find('span', class_='vehicle-price__price').text.replace('$','').replace(',','').strip()
            except:
                boat_msrp = 'N/A'
            try:
                boat_discount = boats.find('span', class_='vehicle-price--current').find('span', class_='vehicle-price__price').text.replace('$', '').replace(',', '').strip()
            except:
                boat_discount = 'N/A'
            try:
                boat_stock = boats.find('li', class_='vehicle-specs__item--stock-number').find('span', class_='vehicle-specs__value').text
            except:
                boat_stock = 'N/A'

            try:    
                boat_length = boats.find('li', class_='vehicle-specs__item--length-overall').find('span', class_='vehicle-specs__value').text
            except:
                boat_length = 'N/A'



            with open(f'DailyFiles/Anderson Power {today}.csv', 'a',newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                if file.tell() == 0:
                    writer.writerow(['Year', 'Company', 'Model','FloorPlan', 'Length','Engine', 'Stock Number','Dealer', 'Location','MSRP','DISCOUNT','Date'])
                
                writer.writerow([boat_year, boat_company,boat_model,boat_floor,boat_length,'N/A',boat_stock,'Anderson Power',boat_location,boat_msrp,boat_discount,today])

        



    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
