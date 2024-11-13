
import scrapy
from scrapy_playwright.page import PageMethod
from bs4 import BeautifulSoup
import math
import urllib.parse
import datetime
import csv
import re
import random

# Generate a string of 5 random numbers between 1 and 100
def num():
    random_numbers = ''.join(str(random.randint(1, 100)) for _ in range(5))


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


class boyersales(scrapy.Spider):
    name = 'boyersales'  # Unique identifier for the spider

    def start_requests(self):
        # Dictionary of URLs the spider will start with
        urls = { 
            'Travel Trailer': 'https://www.boyerrvsales.com/default.asp?condition=new&page=xAllInventory&pg=1&subcategory=travel%20trailer',
            'FifthWheel': 'https://www.boyerrvsales.com/default.asp?condition=new&page=xAllInventory&pg=1&subcategory=fifth%20wheel',
            'ToyHauler': 'https://www.boyerrvsales.com/default.asp?condition=new&page=xAllInventory&pg=1&subcategory=toy%20hauler%20-%20fifth%20wheel&subcategory=toy%20hauler%20-%20travel%20trailer',
            'ClassC Gas': 'https://www.boyerrvsales.com/default.asp?condition=new&page=xAllInventory&pg=1&subcategory=class%20c',
            'ClassB Gas': 'https://www.boyerrvsales.com/default.asp?condition=new&page=xAllInventory&pg=1&subcategory=class%20b',
            'ClassA Gas': 'https://www.boyerrvsales.com/default.asp?condition=new&page=xAllInventory&pg=1&subcategory=class%20a',
            'Destination Trailer' : 'https://www.boyerrvsales.com/default.asp?condition=new&page=xAllInventory&pg=1&subcategory=destination'
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



        for unit in units:
            companyAndBrand = unit.find('span', class_='vehicle-heading__name').text

            manufacturer = None
            for manuf in manufacturer_list:
                if manuf in companyAndBrand:
                    manufacturer = manuf
                    break  # Stop at the first match

            if not manufacturer:
                manufacturer = "Unknown"

            unit_year = unit.find('span', class_='vehicle-heading__year').text.strip()
            unit_company = manufacturer
            unit_brand = find_model(companyAndBrand)
            floor = unit.find('span', class_='vehicle-heading__model').text.strip().split()
            unit_floor = floor[-1]
            try:
                unit_msrp = unit.find('span', class_='vehicle-price--old').text.replace('Retail Price','').replace('$','').replace(",",'').replace('Our Price','').replace('Click for a Quote','').strip()
            except:
                unit_msrp = 'N/A'
            
            try:
                unit_discount = unit.find('span', class_='vehicle-price--current').text.replace('Retail Price','').replace('$','').replace(",",'').replace('Our Price','').replace('Click for a Quote','').strip()
            except:
                unit_discount = 'N/A'

            unit_stock = unit.find('li', class_="vehicle-specs__item vehicle-specs__item--stock-number").find('span', class_="vehicle-specs__value").text

            unit_category = response.meta['category_name']
            unit_location = 'Erie PA'

            with open(f'DailyFiles/Boyersales {today}.csv', 'a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                if file.tell() == 0:  # If file is empty, write header
                    writer.writerow(['Year','Company','Brand','FloorPlan','Msrp','Discount','Stock-Number','Unit Type','Location','Dealer','Date'])
                
                writer.writerow([unit_year,unit_company,unit_brand,unit_floor,unit_msrp,unit_discount,unit_stock,unit_category,unit_location,'Boyersales',today])

        



    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.request.url}")
