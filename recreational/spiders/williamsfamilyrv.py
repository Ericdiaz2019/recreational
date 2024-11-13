import scrapy
from scrapy_playwright.page import PageMethod
from bs4 import BeautifulSoup
import re
import csv
import math
import datetime
import time
import random
today = datetime.date.today()

manufacturer_list = [
    "Airstream RV", "Alliance RV", "American Coach", "Black Series Camper", "Brinkley",
    "Coachmen RV", "CrossRoads RV", "Cruiser", "Dave & Matt Vans", "DRV Luxury Suites",
    "Dynamax", "EAST TO WEST", "Eclipse", "Ember RV", "Entegra Coach", "Fleetwood RV",
    "Forest River RV", "Grand Design", "Grech RV", "Gulf Stream RV", "Heartland",
    "Jayco", "Keystone RV", "Lance", "Midwest Automotive Designs", "Newmar", "NeXus RV",
    "OGV Luxury", "OGV Luxury Coach", "Outside Van", "Palomino", "Phoenix Cruiser",
    "Pleasure-Way", "Prime Time RV", "Regency RV", "Remote Vans", "Renegade",
    "Roadtrek", "Storyteller Overland", "Thor Motor Coach", "Tiffin Motorhomes", "Unknown",
    "Venture RV", "Winnebago", "Winnebago Industries Towables"
]

model_map = {
    "Valor All-Access" : 'Valor All-Access',
    "access": "Access",
    "ace": "ACE",
    "adventurer": "Adventurer",
    "ahara": "Ahara",
    "airstream tb": "Airstream TB",
    "alante": "Alante",
    "allegro": "Allegro",
    "allegro bay": "Allegro Bay",
    "allegro breeze": "Allegro Breeze",
    "allegro bus": "Allegro Bus",
    "allegro red": "Allegro RED",
    "alpine": "Alpine",
    "ameri-lite": "Ameri-Lite",
    "american patriot": "American Patriot",
    "apex nano": "Apex Nano",
    "apex ultra-lite": "Apex Ultra-Lite",
    "approach": "Approach",
    "arcadia": "Arcadia",
    "arcadia select": "Arcadia Select",
    "arcadia super lite": "Arcadia Super Lite",
    "ascent": "Ascent",
    "atlas": "Atlas",
    "atlas-e atl": "Atlas-e ATL",
    "attitude platinum": "Attitude Platinum",
    "attitude pro series": "Attitude Pro Series",
    "avalanche": "Avalanche",
    "avenger": "Avenger",
    "avenger le": "Avenger LE",
    "avenger lt": "Avenger LT",
    "avenue": "Avenue",
    "avenue all-access": "Avenue All-Access",
    "bambi": "Bambi",
    "basecamp": "Basecamp",
    "bay star": "Bay Star",
    "bay star sport": "Bay Star Sport",
    "big country": "Big Country",
    "bighorn": "Bighorn",
    "black series camper": "Black Series Camper",
    "bounder": "Bounder",
    "bt cruiser": "BT Cruiser",
    "bullet": "Bullet",
    "bullet classic": "Bullet Classic",
    "bullet crossfire": "Bullet Crossfire",
    "byway": "Byway",
    "canyon star": "Canyon Star",
    "caravel": "Caravel",
    "carbon": "Carbon",
    "catalina destination series": "Catalina Destination Series",
    "catalina legacy": "Catalina Legacy",
    "catalina legacy edition": "Catalina Legacy Edition",
    "catalina summit 7": "Catalina Summit 7",
    "catalina summit series 7": "Catalina Summit Series 7",
    "catalina summit series 8": "Catalina Summit Series 8",
    "catalina trail blazer": "Catalina Trail Blazer",
    "cedar creek": "Cedar Creek",
    "challenger": "Challenger",
    "chaparral": "Chaparral",
    "chaparral lite": "Chaparral Lite",
    "chateau": "Chateau",
    "cherokee": "Cherokee",
    "cherokee alpha wolf": "Cherokee Alpha Wolf",
    "cherokee black label": "Cherokee Black Label",
    "cherokee grey wolf": "Cherokee Grey Wolf",
    "cherokee wolf den": "Cherokee Wolf Den",
    "cherokee wolf pack": "Cherokee Wolf Pack",
    "cherokee wolf pup": "Cherokee Wolf Pup",
    "classic": "Classic",
    "comet": "Comet",
    "compass": "Compass",
    "compass awd": "Compass AWD",
    "condor": "Condor",
    "conquest class c": "Conquest Class C",
    "cougar": "Cougar",
    "cougar half-ton": "Cougar Half-Ton",
    "cougar sport": "Cougar Sport",
    "cross trail ev": "Cross Trail EV",
    "cross trail xl": "Cross Trail XL",
    "cyclone": "Cyclone",
    "delano sprinter": "Delano Sprinter",
    "delta": "Delta",
    "delta ultra lite": "Delta Ultra Lite",
    "discovery": "Discovery",
    "dutch star": "Dutch Star",
    "dx3": "DX3",
    "dynaquest xl": "DynaQuest XL",
    "eagle": "Eagle",
    "eagle ht": "Eagle HT",
    "ekko": "Ekko",
    "ekko sprinter": "Ekko Sprinter",
    "emblem": "Emblem",
    "embrace": "Embrace",
    "encore": "Encore",
    "entourage": "Entourage",
    "esteem": "Esteem",
    "europa": "Europa",
    "flagstaff": "Flagstaff",
    "flagstaff classic": "Flagstaff Classic",
    "flagstaff classic super lite": "Flagstaff Classic Super Lite",
    "flagstaff e-pro": "Flagstaff E-Pro",
    "flagstaff hard side": "Flagstaff Hard Side",
    "flagstaff macltd series": "Flagstaff MACLTD Series",
    "flagstaff micro lite": "Flagstaff Micro Lite",
    "flagstaff se": "Flagstaff SE",
    "flagstaff shamrock": "Flagstaff Shamrock",
    "flagstaff super lite": "Flagstaff Super Lite",
    "flair": "Flair",
    "flex": "Flex",
    "flying cloud": "Flying Cloud",
    "flying cloud desk": "Flying Cloud Desk",
    "forester": "Forester",
    "forester le": "Forester LE",
    "forester mbs": "Forester MBS",
    "fortis": "Fortis",
    "forza": "Forza",
    "four winds": "Four Winds",
    "fr3": "FR3",
    "fr3 plus": "FR3 Plus",
    "freedom express": "Freedom Express",
    "freedom express liberty edition": "Freedom Express Liberty Edition",
    "freedom express select": "Freedom Express Select",
    "freelander": "Freelander",
    "friendship": "Friendship",
    "fuzion": "Fuzion",
    "gemini": "Gemini",
    "georgetown 5 series": "Georgetown 5 Series",
    "georgetown 7 series": "Georgetown 7 Series",
    "gh1": "GH1",
    "globetrotter": "Globetrotter",
    "granite ridge": "Granite Ridge",
    "grech": "Grech",
    "greyhawk": "Greyhawk",
    "greyhawk xl": "Greyhawk XL",
    "hideout": "Hideout",
    "hideout sport": "Hideout Sport",
    "hideout sport double axle": "Hideout Sport Double Axle",
    "hideout sport single axle": "Hideout Sport Single Axle",
    "imagine": "Imagine",
    "imagine aim": "Imagine AIM",
    "imagine xls": "Imagine XLS",
    "inception": "Inception",
    "independence trail": "Independence Trail",
    "influence": "Influence",
    "international": "International",
    "interstate": "Interstate",
    "interstate 24gl": "Interstate 24GL",
    "interstate 24x": "Interstate 24X",
    "isata 3": "Isata 3",
    "isata 5": "Isata 5",
    "jay feather": "Jay Feather",
    "jay feather air": "Jay Feather Air",
    "jay feather micro": "Jay Feather Micro",
    "jay flight": "Jay Flight",
    "jay flight bungalow": "Jay Flight Bungalow",
    "jay flight slx": "Jay Flight SLX",
    "lance": "Lance",
    "launch": "Launch",
    "leprechaun": "Leprechaun",
    "lineage": "Lineage",
    "lv series": "LV Series",
    "m-series": "M-Series",
    "magnitude": "Magnitude",
    "melbourne": "Melbourne",
    "melbourne prestige": "Melbourne Prestige",
    "micro minnie": "Micro Minnie",
    "midas": "Midas",
    "milestone": "Milestone",
    "minnie": "Minnie",
    "minnie winnie": "Minnie Winnie",
    "mirada": "Mirada",
    "miramar": "Miramar",
    "mobile suites": "Mobile Suites",
    "model g": "Model G",
    "model z": "Model Z",
    "model z air": "Model Z Air",
    "momentum": "Momentum",
    "momentum g-class": "Momentum G-Class",
    "momentum m-class": "Momentum M-Class",
    "momentum mav": "Momentum MAV",
    "montana": "Montana",
    "montana high country": "Montana High Country",
    "new aire": "New Aire",
    "north point": "North Point",
    "odyssey": "Odyssey",
    "omni": "Omni",
    "ontour": "Ontour",
    "open road allegro": "Open Road Allegro",
    "outlaw": "Outlaw",
    "outlaw class c": "Outlaw Class C",
    "overland series": "Overland Series",
    "palomino": "Palomino",
    "paradigm": "Paradigm",
    "passage 144": "Passage 144",
    "passage 144 awd": "Passage 144 AWD",
    "passage 170ext": "Passage 170EXT",
    "passport": "Passport",
    "passport mini": "Passport Mini",
    "phaeton": "Phaeton",
    "phoenix cruiser": "Phoenix Cruiser",
    "pinnacle": "Pinnacle",
    "plateau": "Plateau",
    "pottery barn special edition": "Pottery Barn Special Edition",
    "precept": "Precept",
    "puma": "Puma",
    "puma destination": "Puma Destination",
    "puma ultra lite": "Puma Ultra Lite",
    "puma unleashed": "Puma Unleashed",
    "puma xle lite": "Puma XLE Lite",
    "pursuit": "Pursuit",
    "quantum": "Quantum",
    "qwest": "Qwest",
    "r pod": "R Pod",
    "rangeline": "Rangeline",
    "reatta xl": "Reatta XL",
    "redhawk": "Redhawk",
    "reflection": "Reflection",
    "reflection 100 series": "Reflection 100 Series",
    "reflection 150 series": "Reflection 150 Series",
    "rei special edition basecamp": "REI Special Edition Basecamp",
    "remote vans": "Remote Vans",
    "residence": "Residence",
    "retreat": "Retreat",
    "revel": "Revel",
    "roadtrek": "Roadtrek",
    "rockwood extreme sports": "Rockwood Extreme Sports",
    "rockwood freedom series": "Rockwood Freedom Series",
    "rockwood geo pro": "Rockwood GEO Pro",
    "rockwood hard side high wall series": "Rockwood Hard Side High Wall Series",
    "rockwood hard side series": "Rockwood Hard Side Series",
    "rockwood high wall series": "Rockwood High Wall Series",
    "rockwood limited series": "Rockwood Limited Series",
    "rockwood mini lite": "Rockwood Mini Lite",
    "rockwood otg": "Rockwood OTG",
    "rockwood roo": "Rockwood Roo",
    "rockwood signature": "Rockwood Signature",
    "rockwood ultra lite": "Rockwood Ultra Lite",
    "sabre": "Sabre",
    "sanctuary": "Sanctuary",
    "sandpiper": "Sandpiper",
    "sandpiper destination trailers": "Sandpiper Destination Trailers",
    "scope": "Scope",
    "seismic": "Seismic",
    "seismic luxury": "Seismic Luxury",
    "seismic luxury series": "Seismic Luxury Series",
    "seneca": "Seneca",
    "sequence": "Sequence",
    "solis": "Solis",
    "solis pocket": "Solis Pocket",
    "solitude": "Solitude",
    "solitude s-class": "Solitude S-Class",
    "solstice": "Solstice",
    "sonic": "Sonic",
    "sonic lite": "Sonic Lite",
    "sportscoach srs": "Sportscoach SRS",
    "sporttrek": "SportTrek",
    "sporttrek touring edition": "SportTrek Touring Edition",
    "springdale": "Springdale",
    "springdale classic": "Springdale Classic",
    "springdale classic mini": "Springdale Classic Mini",
    "springdale mini": "Springdale Mini",
    "storyteller overland": "Storyteller Overland",
    "strada": "Strada",
    "strada-ion": "Strada-ion",
    "strada-ion awd": "Strada-ion AWD",
    "stratus": "Stratus",
    "stratus sport": "Stratus Sport",
    "stryker": "Stryker",
    "sunseeker": "Sunseeker",
    "sunseeker classic": "Sunseeker Classic",
    "sunseeker le": "Sunseeker LE",
    "sunseeker mbs": "Sunseeker MBS",
    "sunset trail": "Sunset Trail",
    "super star": "Super Star",
    "supreme aire": "Supreme Aire",
    "swift": "Swift",
    "swift li": "Swift Li",
    "syncline": "Syncline",
    "tellaro": "Tellaro",
    "terrain": "Terrain",
    "terreno awd": "Terreno AWD",
    "terreno-ion awd": "Terreno-ion AWD",
    "tiburon sprinter": "Tiburon Sprinter",
    "timberwolf": "Timberwolf",
    "touring edition": "Touring Edition",
    "trade wind": "Trade Wind",
    "trail boss": "Trail Boss",
    "transcend": "Transcend",
    "transcend one": "Transcend One",
    "transcend xplor": "Transcend Xplor",
    "travato": "Travato",
    "triumph super c": "Triumph Super C",
    "turismo-ion": "Turismo-ion",
    "turismo-ion awd": "Turismo-ion AWD",
    "ultra brougham": "Ultra Brougham",
    "unknown": "Unknown",
    "v-cruise": "V-Cruise",
    "v-rv": "V-RV",
    "valencia": "Valencia",
    "valor": "Valor",
    "valor all-access": "Valor All-Access",
    "vegas": "Vegas",
    "ventana": "Ventana",
    "veracruz": "Veracruz",
    "verona": "Verona",
    "verona le": "Verona LE",
    "view": "View",
    "vintage cruiser": "Vintage Cruiser",
    "vision": "Vision",
    "vision xl": "Vision XL",
    "vista": "Vista",
    "vista cruiser": "Vista Cruiser",
    "vita": "Vita",
    "voyage": "Voyage",
    "wayfarer": "Wayfarer",
    "white hawk": "White Hawk",
    "wildwood": "Wildwood",
    "wildwood fsx": "Wildwood FSX",
    "wildwood heritage glen": "Wildwood Heritage Glen",
    "wildwood lodge": "Wildwood Lodge",
    "wildwood select": "Wildwood Select",
    "wildwood x-lite": "Wildwood X-Lite",
    "windsport": "Windsport",
    "work and play": "Work and Play",
    "xlr boost": "XLR Boost"
}


def find_model(unit_title):
    brand = None
    # Iterate over the model_map keys to find a match in unit_title
    for model_key in model_map:
        if model_key.lower() in unit_title.lower():  # Case-insensitive match
            brand = model_map[model_key]  # Get the normalized model name from model_map
            break  # Stop at the first match
    
    # If no match was found, set brand to 'N/A'
    if not brand:
        brand = 'N/A'

    return brand

proxies = [
    {"server": "134.195.230.104:6066", "username": "DHMR115563", "password": "AIJKMQXZ"},
    {"server": "134.195.229.200:5261", "username": "DHMR115563", "password": "AIJKMQXZ"},
    {"server": "216.185.221.198:6906", "username": "DHMR115563", "password": "AIJKMQXZ"},
    # Add more proxies as necessary
]


class williamsfamilyrv(scrapy.Spider):
    name = "williamsfamilyrv"


    def start_requests(self):
        web_links = {
            'Travel Trailer': 'https://www.williamsfamilyrv.com/rv-search?s=true&condition=1&pagesize=12&types=29',
            'FifthWheel': 'https://www.williamsfamilyrv.com/rv-search?s=true&condition=1&pagesize=12&types=5',
            'ToyHauler': 'https://www.williamsfamilyrv.com/rv-search?s=true&condition=1&pagesize=12&types=26',
            'ClassC Diesel': 'https://www.williamsfamilyrv.com/rv-search?s=true&condition=1&pagesize=12&types=17',
            'ClassB Diesel': 'https://www.williamsfamilyrv.com/rv-search?s=true&condition=1&pagesize=12&types=116',
            'Destination Trailer' : 'https://www.williamsfamilyrv.com/rv-search?s=true&condition=1&pagesize=12&types=3'
        }

        for category_name, link_url in web_links.items():

                yield scrapy.Request(
                    url=link_url,
                    meta={
                        'playwright': True,
                        'playwright_page_methods': [
                            PageMethod("wait_for_selector", "span.total-units"),
                        ],
                        'playwright_context': 'default',
                        'page_goto_kwargs': {'timeout': 60000},   # Use default browser context
                        'category_name': category_name,
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
                    'category_name': response.meta['category_name'],
                },
                callback=self.parse_units,
                errback=self.handle_error,
                dont_filter=True
            )
        
    
    def parse_units(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        units = soup.find_all('li', class_='standard-template-v2')

        for unit in units:
            unit_title = unit.find('div', class_='h3 unit-title').find('a').text.strip()
            unit_title_text = unit_title.split()

            unit_year = unit_title_text[1]

            manufacturer = None
            for manuf in manufacturer_list:
                if manuf in unit_title:
                    manufacturer = manuf
                    break  # Stop at the first match

            if not manufacturer:
                manufacturer = "Unknown"



            unit_company = manufacturer
            unit_brand = find_model(unit_title)
            unit_floor = unit_title_text[-1]
            unit_stock = unit.find('span', class_='stock-number-text').text
            unit_location = unit.find('span', class_='unit-location-text').text.replace('.','').replace(',','').replace('""','').strip()
            unit_category = response.meta['category_name']
            try:
                unit_msrp = unit.find('span', class_='reg-price-text').text.replace('$','').replace(',','').strip()
            except:
                unit_msrp = 'N/A'
            
            try:
                unit_discount = unit.find('span', class_='sale-price-text').text.replace('$','').replace(',','').strip()
            except:
                unit_discount = 'N/A'

            with open(f'DailyFiles/WilliamsFamily {today}.csv', 'a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                if file.tell() == 0:  # If file is empty, write header
                    writer.writerow(['Year','Company','Brand','FloorPlan','Msrp','Discount','Stock-Number','Unit Type','Location','Dealer','Date'])
                
                writer.writerow([unit_year,unit_company,unit_brand,unit_floor,unit_msrp,unit_discount,unit_stock,unit_category,unit_location,'WilliamsFamily',today])

    def handle_error(self, failure):
        self.logger.error(repr(failure))
        self.logger.info('Retrying request...')

