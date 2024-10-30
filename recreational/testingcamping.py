import requests, random, logging, re, os
import datetime

# Setup logging to file
file_handler = logging.FileHandler("log.txt", mode="a")
file_handler.setLevel(logging.INFO)
logging.basicConfig()
logging.root.setLevel(logging.INFO)
file_format = logging.Formatter('%(asctime)s:%(msecs)d %(levelname)s %(message)s')
logger = logging.getLogger("scraper")
logger.addHandler(file_handler)
today = datetime.date.today()

# Load proxies from file
with open("proxies.txt", 'r') as r:
    proxies = r.read().splitlines()

# Manufacturer list
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

# Model mapping
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

# Proxy function
def get_proxy():
    if not proxies:
        return {}

    proxy = random.choice(proxies)
    ip, port, user, password = proxy.split(":")
    proxy = f"http://{user}:{password}@{ip}:{port}"
    proxy = {
        "http": proxy,
        "https": proxy,
    }
    return proxy

# Scraper class
class Scraper:
    def __init__(self, starting_page: int = 1):
        self.starting_page = starting_page
        self.session = requests.session()
        # If no units.csv file create one
        if not os.path.isfile(f"DailyFiles/CampingWorld {today}.csv"):
            self.create_units_csv()

        logger.info("Getting XSRF Token...")
        self.xsrf_token = self.get_xsrf_token()
        self.session.headers.update({
            'accept': '*/*', 'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache', 'content-type': 'application/json',
            'origin': 'https://rv.campingworld.com', 'pragma': 'no-cache',
            'user-agent': 'Mozilla/5.0 ... Safari/537.36',
            'x-auth-token': self.xsrf_token
        })

    @staticmethod
    def create_units_csv() -> None:
        if not os.path.isfile(f"DailyFiles/CampingWorld {today}.csv"):
            with open(f"DailyFiles/CampingWorld {today}.csv", 'w') as r:
                r.write('Year,Company,Brand,FloorPlan,Msrp,Discount,Stock-Number,Unit Type,Location,Dealer,Date\n')

    def get_xsrf_token(self) -> str:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,...,*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Safari/537.36'
        }
        params = {'rv_class': 'tt', 'zip': '23455', 'forcedistance': 'nationwide'}
        response = self.session.get('https://rv.campingworld.com/searchresults', params=params, headers=headers, proxies=get_proxy())
        return "ey" + re.findall('<meta content="ey(.*?)"', response.text)[0]

    def get_page(self, page_num: int) -> dict:
        json_data = {
            'recommended': True,
            'pagination': {'page': page_num, 'take': 12},
            # (other pagination and parameter settings)
        }

        response = self.session.post('https://api.rvs.com/api/v1/asset/search/basic', json=json_data, proxies=get_proxy())
        assets = response.json()['assets']
        if len(assets) == 0:
            return

        return assets

    @staticmethod
    def write_asset_data(asset_data: dict) -> None:
        with open(f"DailyFiles/CampingWorld {today}.csv", 'a') as r:
            r.write(", ".join([str(i) for i in asset_data.values()]))
            r.write("\n")

    # Helper function to find manufacturer
    @staticmethod
    def find_manufacturer(unit_title):
        for manuf in manufacturer_list:
            if manuf.lower() in unit_title.lower():
                return manuf
        return "Unknown"

    # Helper function to find model
    @staticmethod
    def find_model(unit_title):
        for model_key in model_map:
            if model_key.lower() in unit_title.lower():
                return model_map[model_key]
        return "N/A"

    def get_data_from_asset(self, asset_data) -> dict:
        unit_model = asset_data.get('brand', '')
        unit_company = asset_data.get('make','')
        manufacturer = self.find_manufacturer(unit_company)
        brand = self.find_model(unit_model)
        
        data = {
            "Year": asset_data['year'],
            "Company": manufacturer,
            "Brand": brand,
            "FloorPlan": asset_data['model'],
            "MSRP": asset_data['totalListPrice'],
            "Discount Price": asset_data['queryPrice'],
            "stockNumber": asset_data['stockNumber'],
            "Category": asset_data['classDisplay'],
            "Location": f"{asset_data['billingCity']} {asset_data['billingStateCode']}",
            "Dealer": 'Camping World',
            "Date": today,
            "condition": asset_data['condition']
        }
        return data

    def scrape(self) -> None:
        for i in range(self.starting_page, 10000):
            logger.info(f"Getting page {i}...")
            page = self.get_page(i)
            if page is None:
                logger.info("Reached last page, closing...")
                print("Reached last page, closing...")
                return
            else:
                for asset in page:
                    asset_data = self.get_data_from_asset(asset)
                    self.write_asset_data(asset_data)


# Function to run the scraper
def run_scraper(starting_page: int = 1):
    scraper = Scraper(starting_page)
    logger.info("Starting scrape loop...")
    scraper.scrape()


# Entry point for running directly
if __name__ == "__main__":
    run_scraper()
