import subprocess
import datetime
from validation import boatCreateOneFile,rvCreateOneFile
from dataLoad import load_data_daily_pull
from bluecompass import run_bluecompass_scraper
from campingworld import run_scraper
today = datetime.date.today()

def runRvSpiders():
    rvSpiders = ['campersinn', 'bish', 'generalrv', 'alrv', 'arbutus', 'hwhrv', 'lazydays', 'meyers', 'ronhoover', 'parris']

    for spider in rvSpiders:
        subprocess.run(['scrapy', 'crawl', spider])

def runBoatSpiders():
    boatSpiders = ['buckeyesportscenter', 'desmaspider', 'futrellmarine', 'marinekentu', 'lodderspider','spiderviking', 'wickspider', 'spiderlanding', 'settlespider', 'spiderboat', 'spiderford', 'spiderwakeside']

    for spider in boatSpiders:
        subprocess.run(['scrapy', 'crawl', spider])


def runBoatMain():
    runBoatSpiders()
    boatCreateOneFile()
    load_data_daily_pull(f'DailyRun/BoatDaily {today}.csv','DailyBoatPull','Yes')


def runRvMain():
    runRvSpiders()
    run_bluecompass_scraper()
    run_scraper()
    rvCreateOneFile()
    load_data_daily_pull(f'DailyRun/data {today}.csv','DailyPull','Yes')


runRvMain()
