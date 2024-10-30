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
            unit_title = x.find('div', class_='h3 unit-title').find('a').text.strip()
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
            unit_stock = x.find('span', class_='stock-number-text').text
            unit_location = x.find('span', class_='unit-location-text').text.replace('.','').replace(',','').replace('""','').strip()
            try:
                unit_msrp = x.find('span', class_='reg-price-text').text.replace('$','').replace(',','').strip()
            except:
                unit_msrp = 'N/A'
            
            try:
                unit_discount = x.find('span', class_='sale-price-text').text.replace('$','').replace(',','').strip()
            except:
                unit_discount = 'N/A'
            

            results.append((unit_year,unit_company,unit_brand,unit_floor,unit_msrp,unit_discount,unit_stock,self.category,unit_location,'BlueCompass',str(today)))

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
        'Travel Trailer': 'https://www.bluecompassrv.com/new-rvs-for-sale?s=true&types=29&distance=any&pagesize=12&page=1',
        'FifthWheel': 'https://www.bluecompassrv.com/new-rvs-for-sale?s=true&types=5&distance=any&pagesize=12&page=1',
        'ToyHauler': 'https://www.bluecompassrv.com/new-rvs-for-sale?s=true&types=26%2C28&pagesize=12&distance=any&pagesize=12&page=1',
        'ClassC Gas': 'https://www.bluecompassrv.com/rv-search?s=true&types=16&condition=1&distance=any&pagesize=12&page=1',
        'ClassC Diesel': 'https://www.bluecompassrv.com/product/motor-home-class-c?s=true&condition=1&types=17&distance=any&pagesize=12&page=1',
        'ClassC ToyHauler': 'https://www.bluecompassrv.com/product/motor-home-class-c?s=true&condition=1&types=19&distance=any&pagesize=12&page=1',
        'ClassC Super Diesel': 'https://www.bluecompassrv.com/product/motor-home-class-c?s=true&condition=1&types=95&distance=any&pagesize=12&page=1',
        'ClassB Gas': 'https://www.bluecompassrv.com/rv-search?s=true&types=13&condition=1&distance=any&pagesize=12&page=1',
        'ClassB Diesel': 'https://www.bluecompassrv.com/rv-search?s=true&types=116&condition=1&distance=any&pagesize=12&page=1',
        'ClassB Gas+': 'https://www.bluecompassrv.com/rv-search?s=true&types=14&condition=1&distance=any&pagesize=12&page=1',
        'ClassB Diesel+': 'https://www.bluecompassrv.com/rv-search?s=true&types=15&condition=1&distance=any&pagesize=12&page=1',
        'ClassA Gas': 'https://www.bluecompassrv.com/rv-search?s=true&types=9&condition=1&distance=any&pagesize=12&page=1',
        'ClassA Diesel': 'https://www.bluecompassrv.com/rv-search?s=true&types=10&condition=1&distance=any&pagesize=12&page=1',
        'ClassA ToyHauler Gas': 'https://www.bluecompassrv.com/rv-search?s=true&types=12&condition=1&distance=any&pagesize=12&page=1',
        'ClassA ToyHauler Diesel': 'https://www.bluecompassrv.com/rv-search?s=true&types=11&condition=1&distance=any&pagesize=12&page=1',
        'Destination Trailer': 'https://www.bluecompassrv.com/new-rvs-for-sale?s=true&types=3&condition=&distance=anypagesize=12&page=1'
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
