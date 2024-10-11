import datetime
import random
import logging
import re
import os
import tls_client
import threading
import time
from bs4 import BeautifulSoup

# Logger setup
def setup_logger():
    file_handler = logging.FileHandler("log.txt", mode="a")
    file_handler.setLevel(logging.INFO)
    logging.basicConfig()
    logging.root.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s:%(msecs)d %(levelname)s %(message)s')
    logger = logging.getLogger("scraper")
    logger.addHandler(file_handler)
    return logger

logger = setup_logger()
dic_brands = {
            'Thor Motor Coach' : 'Thor-Motor-Coach',
            'Forest River RV': 'Forest-River-Rv',
            'Braxton Creek': 'Braxton-Creek',
            'BRAXTON CREEK RV, LLC' : 'Braxton-Creek',
            'BLACK SERIES' : 'Black-Series',
            'Coleman RV': 'Coleman-RV',
            'nuCamp RV': 'nuCamp-RV',
            'Coachmen RV': 'Coachmen',
            'Dutchmen RV': 'Dutchmen',
            'Cruiser Twilight': 'Cruiser-Twilight',
            'Grand Design': 'Grand-Design',
            'Winnebago Industries': 'Winnebago-Industries',
            'CrossRoads RV': 'Crossroads-RV',
            'Airstream RV': 'Airstream',
            'Highland Ridge RV': 'Highland-Ridge-RV',
            'FOREST RIVER': 'Forest-River-RV',
            'AIRSTREAM RV': 'Airstream-RV',
            'Olympia Olympia': 'Olympia-RV',
            'Olympia' : 'Olympia-RV',
            'PALOMINO' : 'Palomino-RV',
            'PRIME' : 'Prime-Time-RV',
            'Riverside' : 'Riverside-RV',
            'Venture' : 'Venture-RV',
            'Winnebago-Industries' : 'Winnebago',
            'Keystone RV': 'Keystone',
            'Hero Camper': 'HERO',
            'GRAND DESIGN': 'Grand-Design',
            'KEYSTONE RV': 'Keystone',
            'Alliance RV': 'Alliance-RV',
            'VanLeigh RV': 'VanLeigh-RV',
            'CROSSROADS RV': 'Crossroads-RV',
            'DRV MOBILE': 'DRV',
            'Palomino': 'Palomino-RV',
            'Prime Time RV': 'Prime-Time-RV',
            'Jayco': 'Jayco',
            'Heartland': 'Heartland-RV',
            'Redwood RV': 'Redwood-RV',
            'BRAXTON CREEK': 'Braxton-Creek',
            'Forest River' : 'Forest-River-Rv',
            'EMBER RECREATIONAL' : 'Ember-Rv',
            'Ember RV' : 'Ember-Rv',
            'Riverside RV' : 'Riverside-RV',
            'Encore RV' : 'Encore-RV',
            'InTech RV' : 'Intech',
            'Holiday House RV' : 'Holiday-House-RV',
            'Vanleigh RV' : 'Vanleigh-RV',
            'KZ RV' : 'KZ',
            'Cruiser RV' : 'Cruiser-RV',
            'EAST TO WEST' : 'East-to-west',
            'VENTURE RV' : 'Venture-RV',
            'MSRP' : ' ',
            'Clearance Pricing!' : ' ', 
            'Lowest Priced in the Market' : ' ',
            'Mod Bug Vans' : 'Mod-Bug-Vans',
            'Shasta RVs'  : 'Shasta-RV',
            'Forest River RV' : 'Forest-River-Rv',
            'Grand Design' :'Grand-Design',
            'Gulf Stream' : 'Gulf-Stream',
            'Tiffin Motorhomes' : 'Tiffin-Motorhomes',
            'Entegra Coach' : 'Entegra-Coach',
			'grand design' : 'Grand-Design',
			'forest river rv' : 'Forest-River-Rv',
			'jayco' : 'Jayco',
			'keystone rv' : 'Keystone'
        }
dic_floor = {
            'JAY SERIES' : 'Jay-Series',
            'JAY FLIGHT' : 'Jay-Flight',
            'NO BOUNDARIES' : 'No-Boundaries',
            'WHITE HAWK': 'White-Hawk',
            'JAY FEATHER': 'Jay-Feather',
            'Suites 40': 'Suites-40',
            'Suites 41': 'Suites-41',
            'Suites MS': 'Suites-MS',
            'Ultra Lite': 'Ultra-Lite',
            '150 Series': '150-Series',
            'Heritage Glen': 'Heritage-Glen',
            'XLE Lite': 'XLE-Lite',
            'Mini Lite': 'Mini-Lite',
            'Micro Lite': 'Micro-lite',
            'Super Lite': 'Super-Lite',
            'Special Edition': 'Special-Edition',
            'Range Light': 'Range-Light',
            '25RB Twin': '25RB-Twin',
            '28RB Twin': '28RB-Twin',
            '30FB Twin': '30FB-Twin',
            'Barn Special': 'Barn-Special',
            'Geo Pro': 'Geo-Pro',
            'Edition 28RB': 'Edition-28RB',
            'Edition 28RB Twin': 'Edition-28RB-Twin',
            'Plus ROMO': 'Plus-Romo',
            'SLX 7': 'SLX-7',
            'RANGER W SKYBOX': 'RANGER-W-SKYBOX',
            'HERO RANGER W': 'HERO-RANGER-W',
            'Lite Air': 'Lite-Air',
            'Micro Minnie': 'Micro-Minnie',
            'Freedom Express': 'Freedom-Express',
            'Micro Minnie FLX': 'Micro-Minnie-FLX',
            'HQ Series HQ15': 'HQ15',
            'SOLO PLUS': 'SOLO-PLUS',
            'XLE Lite': 'XLE-Lite',
            # 'Basecamp 16' : 'Basecamp-16',
            'Jay Flight': 'Jay-Flight',
            'Jay Feather': 'Jay-Freather',
            'Transcend Xplor': 'Transcend-Xplor',
            'Signature TWS': 'Signature-TWS',
            'Flying Could': 'Flying Cloud',
            'Imagine XLS': 'Imagine-XLS',
            'XLR HYPER Lite' : 'XLR-HYPER-Lite',
            'Eagle HT': 'Eagle-HT',
            '30FB Bunk': '30FB-Bunk',
            'GEO Pro': 'Geo-Pro',
            '30FB Office': '30FB-Office',
            'Flight SLX 7': 'Flight-SLX-7',
            'HERO RANGER': 'HERO RANGER',
            'Flight SLX': 'Flight-SLX',
            'FLX 2108FBS': 'FLX-2108FBS',
            'FLX 2108FDS': 'FLX-2108FDS',
            'FLX 2108DS': 'FLX-2108DS',
            'FLX 2100BH': 'FLX-2100BH',
            'FLX 2108TB': 'FLX-2108TB',
            'FLX 2306BHS': 'FLX-2306BHS',
            'Solo Plus': 'Solo-Plus',
            '25FB Twin': '25FB-Twin',
            'HERO RANGER': 'HERO-RANGER',
            '273 RL': '273-RL',
            'Micro Boost': 'Micro-Boost',
            'Work and Play': 'Work-and-Play',
            'Wolf Pup': 'Wolf-Pup',
            'Wolf Pup Black Label': 'Wolf-Pup-Black-Label',
            'Black Label': 'Black-Label',
            "Arctic Wolf": 'Arctic-Wolf',
            'Open Range': 'Open-Range',
            'High Country': 'High Country',
            "Arctic Wolf Suite": 'Arctic-Wolf-Suite',
            'Rockwood Signature': 'Rockwood-Signature',
            'Mesa Ridge': 'Mesa-Ridge',
            'Alpha Wolf': 'Alpha-Wolf',
            'Apex Nano': 'Apex-Nano',
            'Freedom Express': 'Freedom-Express',
            'Grey Wolf': 'Grey-Wolf',
            'Wolf Pup': 'Wold-Pup',
            'Lance Lance': 'Lance',
            'Travel Trailers': 'Travel-Trailers',
            'Touring Edition': 'Touring-Edition',
            'R Pod': 'R-Pod',
            '19 QBS': '19-QBS',
            'DRV Luxury Suites': 'DRV-Luxury-Suites',
            'Range Roamer': 'Range-Roamer',
            'Signature Ultra': 'Signature-Ultra',
            'High Country': 'High-Country',
            'inTech RV': 'intech',
            'INTECH RV': 'intech',
            'SALEM GRAND VILLA' : 'Salem-Grand-Villa',
            'North Trail' : 'North-Trail',
            'The Beacon' : 'The-Beacon',
            'E PRO' : 'E-Pro',
            'ALL TYPES OF CREDIT ACCEPTED' : ' ',
            'In-Store' : ' ',
            'Ultra Lightweight!' : ' ',
            'EMBER RV' : 'Ember-Rv',
            'ALLIANCE RV' : 'Alliance-RV',
            'Lowest Priced in the market' : ' ',
            'Unbeatable Savings, Unbeatable Value' : ' ',
            'CrossRoads Rv' : 'Crossroads-RV',
            'GREY WOLF' : 'Grey-Wolf',
            'In-Store Hail Discount' : ' ',
            'Ultra Lightweight!' : ' ',
            'TRAVEL LITE' : 'Travel-Lite',
            'FLAGSTAFF MICRO' : 'Flagstaff-Micro',
            'MICRO MINNIE' : 'Micro-Minnie',
            'CRUISER RV' : 'Cruiser-RV',
            'VENTURE RV' : 'Venture-RV',
            'SPORT TREK' : 'Sport-Trek',
            'HIKE 100' : 'Hike-100',
            'Hail Discount' : ' ',
            '$68,980.00' : ' ',
        }

today = datetime.date.today()

# Thread lock for writing to file
LOCK = threading.Lock()

# Load proxies
def load_proxies():
    with open("proxies.txt", 'r') as r:
        return r.read().splitlines()

proxies = load_proxies()

# Get a random proxy from the list
def get_proxy():
    if not proxies:
        return {}

    proxy = random.choice(proxies)
    ip, port, user, password = proxy.split(":")
    proxy_url = f"http://{user}:{password}@{ip}:{port}"
    return {
        "http": proxy_url,
        "https": proxy_url,
    }

# Create the CSV file if it doesn't exist
def create_units_csv() -> None:
    if not os.path.isfile(f'DailyFiles/Bluecompass RV {today}.csv'):
        with open(f'DailyFiles/Bluecompass RV {today}.csv', 'w') as r:
            r.write(f'Year, Company, Brand, FloorPlan, Msrp, Discount, Stock-Number, Unit Type, Location, Dealer, Date\n')

# Add a line to the CSV file
def add_line_to_csv(line: str):
    with LOCK:
        with open(f'DailyFiles/Bluecompass RV {today}.csv', 'a') as r:
            r.write(f"{line}\n")

# Scraper class
class Scrape:
    def __init__(self, category: str, url: str, starting_page: int = 1):
        self.starting_page = starting_page
        self.session = tls_client.Session(
            client_identifier=random.choice(['chrome_103', 'chrome_104', 'chrome_105', 'chrome_106', 'chrome_107', 'chrome_108', 'chrome109', 'Chrome110', 'chrome111', 'chrome112', 'chrome_116_PSK', 'chrome_116_PSK_PQ', 'chrome_117', 'chrome_120', 'firefox_102', 'firefox_104', 'firefox108', 'Firefox110', 'firefox_117', 'firefox_120']),
            random_tls_extension_order=True
        )
        self.session.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        })
        self.category = category
        self.url = url

    def get_page(self, page_num: int) -> str:
        url = self.url[:-1] + str(page_num)
        attempts = 0
        while True:
            response = self.session.post(url, proxy=get_proxy())
            attempts += 1
            if response.status_code != 200:
                logger.error(f"{self.category}: {response.status_code} Error getting page, retrying...")
                time.sleep(5 * attempts)
            else:
                logger.info(f"{self.category}: Got page {page_num}")
                return response.text

    def get_details_from_body(self, body: str) -> list:
        f = BeautifulSoup(body, 'lxml')
        unit_li = f.find_all('li', class_='standard-template-v2')
        results = []

        for x in unit_li:
            title_div = x.find_all('div', class_='h3 unit-title')
            title = title_div[0].find('a').text.lower()

            location_element = x.find('span', class_='unit-location-text')
            location = location_element.text.strip() if location_element and location_element.text.strip() != '' else 'N/A'

            xlot = x.find('span', class_='stock-number-text')
            lot = 'Not Lot' if not xlot else xlot.text

            regular_price = x.find('span', class_='reg-price-text')
            regular = 'N/A' if not regular_price else re.sub(r'[^0-9.]', '', regular_price.text)

            discount_price = x.find('span', class_='sale-price-text')
            discounted = 'N/A' if not discount_price else re.sub(r'[^0-9.]', '', discount_price.text)

            groups = re.findall('"manufacturer": "(.*?)",', body)
            brands = re.findall('"brand": "(.*?)",', body)
            manufacturers = list(set(groups))
            brands = list(set(brands))

            manufacturer = "N/A"
            for i in manufacturers:
                if i in title:
                    title = title.replace(i, "")
                    manufacturer = i
                    break

            for old_word, new_word in dic_brands.items():
                manufacturer = manufacturer.replace(old_word, new_word)

            year = title.split()[1:][0]
            floor = title.split()[-1]

            model = "N/A"
            title = " ".join(title.split()[2:])
            brand = "N/A"
            for i in brands:
                if i in title:
                    brand = i
                    break

            if len(brand.split()) == 2:
                brand, model = brand.split()

            today = datetime.date.today()
            results.append((year, manufacturer, brand, model, floor, regular, discounted, lot, self.category, location, 'BlueCompass RV', today.isoformat(),))

        return results

    def do_scrape(self):
        logger.info(f"{self.category}: Starting scraper...")
        for i in range(self.starting_page, 10000):
            logger.info(f"{self.category}: Getting page {i}")
            page_body = self.get_page(i)
            details_list = self.get_details_from_body(page_body)
            if not details_list:
                logger.info(f"{self.category}: Completed scraping.")
                break
            for details in details_list:
                add_line_to_csv(",".join(details))

# Function to run the scraper
def run_bluecompass_scraper():
    # Predefined URLs within the file
    urls = {
        'travelTrailer': 'https://www.bluecompassrv.com/new-rvs-for-sale?s=true&types=29&distance=any&pagesize=12&page=1',
        'fifthWheel': 'https://www.bluecompassrv.com/new-rvs-for-sale?s=true&types=5&distance=any&pagesize=12&page=1',
        'toyHauler': 'https://www.bluecompassrv.com/new-rvs-for-sale?s=true&types=26%2C28&pagesize=12&distance=any&pagesize=12&page=1',
        'classCGas': 'https://www.bluecompassrv.com/rv-search?s=true&types=16&condition=1&distance=any&pagesize=12&page=1',
        'classCDiesel': 'https://www.bluecompassrv.com/product/motor-home-class-c?s=true&condition=1&types=17&distance=any&pagesize=12&page=1',
        'classCToyHauler': 'https://www.bluecompassrv.com/product/motor-home-class-c?s=true&condition=1&types=19&distance=any&pagesize=12&page=1',
        'classCSuperDiesel': 'https://www.bluecompassrv.com/product/motor-home-class-c?s=true&condition=1&types=95&distance=any&pagesize=12&page=1',
        'classBGas': 'https://www.bluecompassrv.com/rv-search?s=true&types=13&condition=1&distance=any&pagesize=12&page=1',
        'classBDiesel': 'https://www.bluecompassrv.com/rv-search?s=true&types=116&condition=1&distance=any&pagesize=12&page=1',
        'classBGas+': 'https://www.bluecompassrv.com/rv-search?s=true&types=14&condition=1&distance=any&pagesize=12&page=1',
        'classBDiesel+': 'https://www.bluecompassrv.com/rv-search?s=true&types=15&condition=1&distance=any&pagesize=12&page=1',
        'classAGas': 'https://www.bluecompassrv.com/rv-search?s=true&types=9&condition=1&distance=any&pagesize=12&page=1',
        'classADiesel': 'https://www.bluecompassrv.com/rv-search?s=true&types=10&condition=1&distance=any&pagesize=12&page=1',
        'classAToyHaulerGas': 'https://www.bluecompassrv.com/rv-search?s=true&types=12&condition=1&distance=any&pagesize=12&page=1',
        'classAToyHaulerDiesel': 'https://www.bluecompassrv.com/rv-search?s=true&types=11&condition=1&distance=any&pagesize=12&page=1',
        'destinationTrailer': 'https://www.bluecompassrv.com/new-rvs-for-sale?s=true&types=3&condition=&distance=anypagesize=12&page=1'
    }

    if not os.path.isfile(f"DailyFiles/Bluecompass RV {today}.csv"):
        create_units_csv()

    for category, url in urls.items():
        scrape = Scrape(category, url)
        scrape.do_scrape()
        time.sleep(5)

# Entry point
if __name__ == "__main__":
    run_bluecompass_scraper()
