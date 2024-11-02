import requests
from bs4 import BeautifulSoup
import math
import re

boat_naming = {
    'Barletta Boats' : 'Barletta',
    '21 RL' : '21RL',
    '21 RL Sport' : '21RL-Sport',
    '21 L' : '21L',
    '23 WRL' : '23WRL',
    '23 RL Sport' : '23RL-Sport',
    '210 CS' : '210CS',
    '230 Sport' : '230-Sport',
    '23 XT' : '23XT',
    '235 SINGLE FLIP LOUNGE' : 'SINGLE-FLIP-LOUNGE'
}

def runPowerLodger():
    # start url         
    url = "https://www.powerlodgeramsey.com/search/inventory/availability/In%20Stock/sort/discount/type/Pontoons/type/Boats/usage/New/page/1"


    # Send a GET request to the URL
    response = requests.get(url)
    page_content = response.text
    soup = BeautifulSoup(page_content, 'lxml')
    label = soup.find('label', class_='search-results-count').text
    total_unit = label.split("of")[-1].split()[0]
    amount = math.ceil(int(total_unit)/ 30)
    print(amount)
    for i in range(amount):
        print(i)
        go_to = requests.get(f'https://www.powerlodgeramsey.com/search/inventory/availability/In%20Stock/sort/discount/type/Pontoons/type/Boats/usage/New/page/{i}')
        page = go_to.text
        soup = BeautifulSoup(page, 'lxml')
        boats = soup.find_all('div', class_='unit-card')

        for boat in boats:

            title = boat.find('h3', class_='results-heading').text.strip().split()
            boat_year = title[0]
            boat_company = title[-1] 
            boat_model = f'{title[1]} {title[2]}'
            boat_floor = 'N/A'
            print(boat)
            boat_engine = 'N/A'
            boat_stock = ''




    

    # Write the HTML response to a text file
    with open("response_page.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
        #writer.writerow([boat_year, boat_company,boat_model,boat_floor,boat_length,boat_engine,boat_stock,'Buckeye Sports',boat_location,boat_msrp,boat_discount,today])



