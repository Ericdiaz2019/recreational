import requests, random, logging, re, os
import datetime

file_handler = logging.FileHandler("log.txt", mode="a")
file_handler.setLevel(logging.INFO)
logging.basicConfig()
logging.root.setLevel(logging.INFO)
file_format = logging.Formatter('%(asctime)s:%(msecs)d %(levelname)s %(message)s')
logger = logging.getLogger("scraper")
logger.addHandler(file_handler)
today = datetime.date.today()

with open("proxies.txt", 'r') as r:
	proxies = r.read().splitlines()


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


class Scraper:
	def __init__(self, starting_page: int = 1):
		self.starting_page = starting_page
		self.session = requests.session()
		# If no units.csv file create one
		if not os.path.isfile(f"DailyFiles/CampingWorld {today}.csv"):
			self.create_units_csv()

		logger.info("Getting XSRF Token...")
		self.xsrf_token = self.get_xsrf_token()
		self.session.headers.update({'accept': '*/*', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'no-cache', 'content-type': 'application/json', 'origin': 'https://rv.campingworld.com', 'pragma': 'no-cache', 'priority': 'u=1, i', 'referer': 'https://rv.campingworld.com/', 'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36', 'x-auth-token': self.xsrf_token})

	@staticmethod
	def create_units_csv() -> None:
		if not os.path.isfile(f"DailyFiles/CampingWorld {today}.csv"):
			with open(f"DailyFiles/CampingWorld {today}.csv", 'w') as r:
				r.write(f'Year','Company','Brand','FloorPlan','Msrp','Discount','Stock-Number','Unit Type','Location','Dealer','Date')
				r.write("\n")

	def get_xsrf_token(self) -> str:
		"""
		Sets the xsrf cookie for the future scraping requests
		:return:
		"""
		headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-language': 'en-US,en;q=0.9', 'cache-control': 'no-cache', 'pragma': 'no-cache', 'priority': 'u=0, i', 'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
		params = {'rv_class': 'tt', 'zip': '23455', 'forcedistance': 'nationwide'}
		response = self.session.get('https://rv.campingworld.com/searchresults', params=params, headers=headers, proxies=get_proxy())

		return "ey" + re.findall('<meta content="ey(.*?)"', response.text)[0]

	def get_page(self, page_num: int) -> dict:
		json_data = {
			'recommended': True,
			'pagination': {
				'page': page_num,
				'take': 12,
			}, 'sort': [], 'parameters': [{'comparisonOperator': '=', 	'value': '23455', 	'field': 'zipCode', }, {'comparisonOperator': '<=', 	'value': '999999', 	'field': 'distanceMiles', }, { 	'comparisonOperator': 'in', 	'value': 'tt', 	'field': 'rvClass', }, { 	'comparisonOperator': 'in', 	'value': 1, 	'field': 'domainId', },],
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

	@staticmethod
	def get_data_from_asset(asset_data) -> dict:
		data = {
			"Year": asset_data['year'],"Company": asset_data['make'],"Brand": asset_data['brand'], "FloorPlan": asset_data['model'],"MSRP": asset_data['totalListPrice'],"Discount Price": asset_data['queryPrice'],"stockNumber": asset_data['stockNumber'],"Category": asset_data['classDisplay'],"Location": f"{asset_data['billingCity']} {asset_data['billingStateCode']}","Dealer": 'Camping World',"Date": today,"condition": asset_data['condition']
			}
		return data

	def scrape(self) -> None:
		for i in range(self.starting_page, 10000):  # Loop til page 10000 or page is empty
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