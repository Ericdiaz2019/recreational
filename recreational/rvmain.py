import subprocess
import datetime
from validation import boatCreateOneFile,rvCreateOneFile, rvValidate, boatValidate
from dataLoad import load_data_daily_pull,load_data_daily_pull_boat
from bluecompass import run_bluecompass_scraper
from testingcamping import run_scraper
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

def runRvSpiders():
    rvSpiders = ['campersinn', 'bish', 'generalrv', 'alrv', 'arbutus', 'hwhrv', 'lazydays', 'meyers', 'ronhoover', 'parris','wilkinsrv']

    for spider in rvSpiders:
        subprocess.run(['scrapy', 'crawl', spider])

def runBoatSpiders():
    boatSpiders = ['buckeyesportscenter', 'desmaspider', 'futrellmarine', 'marinekentu', 'lodderspider','spiderviking', 'wickspider', 'spiderlanding', 'settlespider', 'spiderboat', 'spiderford', 'spiderwakeside','revolutionMarine','montanaBoatCenter',
                   'unionMarine','valleyMarine','waterWorld','riverCity','harrisonMarine','hawkeye','clearLake','slcBoats','blmBoats','mattasMarine','westCost','actionWater','andersonPower','wmf','westorlando','wayzatamarine','waterworkzmarine','watereeMarine',
                   'shybeaver','route1motorsports','planomarine','perfectCatch','paradiseMarine','northpointwatersports','mountainautoandmarine','marinespecialist','leadersrpm','inlandBoat','hillyersmidcitymotorsports','grandpasMarine', 'germainemarine',
                   'gainesvilleMarina','funnsunboats','delandMotors','captainschoiceboats','bryansMarine','brainerdsports','boatandmotorsuperstores','berkeley','barnesMarine','augustaMarine','atlantaMarine','appletonboats','anchorageyachtbasin']

    for spider in boatSpiders:
        subprocess.run(['scrapy', 'crawl', spider])


def runBoatMain():
    runBoatSpiders()
    boatCreateOneFile()
    load_data_daily_pull_boat(f'DailyRun/BoatDaily {today}.csv','DailyBoatPull','Yes')


def runRvMain():
    runRvSpiders()
    run_bluecompass_scraper()
    run_scraper()
    rvCreateOneFile()
    load_data_daily_pull(f'DailyRun/data {today}.csv','DailyPull','Yes')

#load_data_daily_pull_boat(f'DailyRun/BoatDaily {today}.csv','DailyBoatPull','Yes')

#runBoatMain()
runRvMain()
#rvValidate()