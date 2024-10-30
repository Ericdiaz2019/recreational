import subprocess
import datetime
from validation import boatCreateOneFile,rvCreateOneFile, rvValidate, boatValidate
from dataLoad import load_data_daily_pull,load_data_daily_pull_boat
from bluecompass import run_bluecompass_scraper
today = datetime.date.today()

def runRvSpiders():
    rvSpiders = ['campersinn', 'bish', 'generalrv', 'alrv', 'arbutus', 'hwhrv', 'lazydays', 'meyers', 'ronhoover', 'parris','wilkinsrv']

    for spider in rvSpiders:
        subprocess.run(['scrapy', 'crawl', spider])

def runBoatSpiders():
    boatSpiders = ['buckeyesportscenter', 'desmaspider', 'futrellmarine', 'marinekentu', 'lodderspider','spiderviking', 'wickspider', 'spiderlanding', 'settlespider', 'spiderboat', 'spiderford', 'spiderwakeside','revolutionMarine','montanaBoatCenter',
                   'unionMarine','valleyMarine','']

    for spider in boatSpiders:
        subprocess.run(['scrapy', 'crawl', spider])


def runBoatMain():
    runBoatSpiders()
    boatCreateOneFile()
    #boatValidate()
    #load_data_daily_pull(f'DailyRun/BoatDaily {today}.csv','DailyBoatPull','Yes')


def runRvMain():
    runRvSpiders()
    run_bluecompass_scraper()
    rvCreateOneFile()
    load_data_daily_pull(f'DailyRun/data {today}.csv','DailyPull','Yes')


load_data_daily_pull_boat(f'DailyRun/BoatDaily {today}.csv','DailyBoatPull','Yes')
#runBoatMain()
#runRvMain()
#rvValidate()