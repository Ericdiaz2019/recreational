import scrapy
from scrapy_playwright.page import PageMethod
from bs4 import BeautifulSoup
import math
import urllib.parse
import datetime
import csv


today = datetime.date.today()

class futrellmarine(scrapy.Spider):
    name = 'futrellmarine'  # Unique identifier for the spider
    
    def start_requests(self):
        # Dictionary of URLs the spider will start with
        urls = { 
            'Pontoon': 'https://www.futrellmarine.com/boats-for-sale/New/?boatclasscode=Pontoon+Boats&option=100',  # Add more URLs as needed
        }
        for category_name, url in urls.items():
            yield scrapy.Request(
                url=url,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", "div.result-status"),
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

        # Find the div with class 'result-status'
        div_total = soup.find('div', class_='result-status')
        # Get the Span
        div_span = div_total.find('span').text
        # Split the Span text
        span = div_span.split()
        # Total amount of stock is at index 0
        total_amount = span[0]
        # Calculate the number of pages (assuming 100 items per page)
        pages_qty = math.ceil(int(total_amount) / 100)
        
        self.logger.info(f'Total Pages To Scrape: {pages_qty}')

        # Parse the query parameters from the URL
        parsed_url = urllib.parse.urlparse(response.url)
        query_params = dict(urllib.parse.parse_qsl(parsed_url.query))

        # Loop through all pages and update the page number as a query parameter
        for i in range(1, pages_qty + 1):
            query_params['page'] = i  # Add or update the 'page' query parameter
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
                        PageMethod("wait_for_selector", "div.result-status"),
                    ],
                    'category_name': response.meta['category_name']
                },
                callback=self.parse_units,
                errback=self.handle_error,
                dont_filter=True
            )

    def parse_units(self, response):
        # This is where you can parse the data from each page
        self.logger.info(f"Processing units for page: {response.url}")
        soup = BeautifulSoup(response.text, 'lxml')
        units = soup.find_all('div', class_='inventory-model-single')



        for boats in units:
            boat_stock = boats.get('data-boat-stock-number')
            boat_year = boats.get('data-boat-year')
            boat_company = boats.get('data-boat-make').replace('®','').replace('™','')
            boat_model = boats.get('data-boat-model').replace('®','').replace('™','')
            boat_category = response.meta['category_name']
            boat_length = boats.find('div', class_='length-ft').text.replace('"','').replace("'",'').strip()
            boat_msrp = boats.find('div', class_='main-boat-price').text.strip().replace('$','').replace('Request Price', 'N/A')
            boat_location = boats.find('div', class_='boat-location').text.strip()

            with open(f'DailyFiles/Futrell Marine {today}.csv', 'a',newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                if file.tell() == 0:
                    writer.writerow(['Year', 'Company', 'Model','Floor', 'Length','Engine', 'Stock Number','Dealer', 'Location','MSRP','DISCOUNT','Date'])
                
                writer.writerow([boat_year, boat_company,boat_model,'N/A',boat_length,'N/A',boat_stock,'Futrell Marine',boat_location,boat_msrp,'N/A',today])

        



    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
