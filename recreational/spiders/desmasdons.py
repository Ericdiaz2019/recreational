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
            boat_info = boat_info.replace(old_name, new_name).replace('�','')
    
    return boat_info

class desmaspider(scrapy.Spider):
    name = 'desmaspider'  # Unique identifier for the spider
    
    def start_requests(self):
        # Dictionary of URLs the spider will start with
        urls = { 
            'Pontoon': 'https://www.desmasdons.com/default.asp?page=xNewInventory#page=xNewInventory&vc=pontoon',  # Add more URLs as needed
        }

        for category_name, url in urls.items():
            yield scrapy.Request(
                url=url,
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod("wait_for_selector", "span.Units"),
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
        span_total = soup.find('span', class_='Units').text
        # Get the Span
        number = re.search(r'\d+', span_total).group()
        total_amount = number
        # Calculate the number of pages (assuming 100 items per page)
        pages_qty = math.ceil(int(total_amount) / 15)
        
        self.logger.info(f'Total Pages To Scrape: {pages_qty}')

        # Parse the URL and query parameters
        parsed_url = urllib.parse.urlparse(response.url)
        query_params = dict(urllib.parse.parse_qsl(parsed_url.query))

        # Loop through all pages and update the 'p' (page) query parameter
        for i in range(1, pages_qty + 1):
            query_params['p'] = i  # Update the 'p' (page) query parameter
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
                        PageMethod("wait_for_selector", "span.Units"),
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
        units = soup.find_all('div', class_='vehicle_row')



        for boats in units:
            
            title_tag = boats.find('div', class_='unitTitle').find('a').text.strip()
            clean_naming = clean_boat_name(title_tag)
            boat_info = clean_naming.split()
            boat_year = boat_info[0]
            boat_company = boat_info[1]
            boat_company = boat_company.replace('®','').replace('™','')
            if (len(boat_info) == 3):
                boat_model = 'N/A'
                boat_floor = boat_info[2]
                boat_floor = boat_floor.replace('®','').replace('™','')
            else:
                boat_model = boat_info[2]
                boat_model = boat_model.replace('®','').replace('™','')
                boat_floor = boat_info[3]
                boat_floor = boat_floor.replace('®','').replace('™','')
            boat_location = boats.find('span', class_='InvDistance').text.strip()
            boat_category = response.meta['category_name']
            try:
                boat_stock = boats.find('li', class_='stockno').find('span', class_='unitValue').text
            except:
                boat_stock = 'N/A'
            try:
                boat_length = boats.find('li', class_='InvLength').find('span', class_='unitValue').text.replace('"','').replace("'","").strip()
            except:
                boat_length = 'N/A'
            try:
                boat_engine = boats.find('li', class_='InvEngine').find('span', class_='engineValue').text.strip()
            except:
                boat_engine = 'N/A'

            boat_msrp = boats.find('div', class_='InvPrice').find('a').text.replace('Click for Quote!', 'N/A').replace('$','').replace(',','').strip()
                            
            #boat_length = boats.find('div', class_='length-ft').text.strip()

            with open(f'DailyFiles/DesmasDons {today}.csv', 'a',newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                if file.tell() == 0:
                    writer.writerow(['Year', 'Company', 'Model','FloorPlan', 'Length','Engine', 'Stock Number','Dealer', 'Location','MSRP','DISCOUNT','Date'])
                
                writer.writerow([boat_year, boat_company,boat_model,boat_floor,boat_length,boat_engine,boat_stock,'Desmasdons',boat_location,boat_msrp,'N/A',today])

        



    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
