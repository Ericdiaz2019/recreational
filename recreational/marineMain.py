import sys
import asyncio
import datetime

# Set the event loop to SelectorEventLoop on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Set the asyncio reactor before importing Scrapy components
from twisted.internet import asyncioreactor
asyncioreactor.install()

# Now import the Scrapy components
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.buckeye import buckeyesportscenter
from spiders.desmasdons import desmasDons
from spiders.futrellMarine import futrellMarine
from spiders.marineKentu import marineKentu
from spiders.marineLodder import marineLodder
from spiders.marineViking import marineViking
from spiders.marineWick import marineWick
from spiders.moose import mooselanding
from spiders.seattleboats import seattleboats
from spiders.spicersBoat import spicersBoat
from spiders.timsford import timsFord
from spiders.wakeSide import wakeside
from twisted.internet import reactor, defer
from twisted.internet.task import deferLater

# Now import Data cleaner
from validation import boatCreateOneFile

# Now Import Data uploader to Mongo
from dataLoad import load_data_daily_pull
today = datetime.date.today()

def run_spiders_in_sequence():
    process = CrawlerProcess(get_project_settings())

    def crawl_next(spider):
        if spider:
            process.crawl(spider)
            deferLater(reactor, 5, lambda: crawl_next(next_spider()))  # 5-second delay between spiders
        else:
            reactor.stop()

    spiders = [buckeyesportscenter, desmasDons, futrellMarine, marineKentu, marineLodder,marineViking, marineWick, mooselanding, seattleboats, spicersBoat, timsFord, wakeside]

    def next_spider():
        return spiders.pop(0) if spiders else None

    crawl_next(next_spider())
    process.start()


run_spiders_in_sequence()
boatCreateOneFile()
load_data_daily_pull(f'DailyRun/BoatDaily {today}','DailyBoatPull','Yes')