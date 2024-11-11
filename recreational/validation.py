import csv
import datetime

def rvValidate():

    # Get today's date
    today = datetime.date.today()

    # Calculate yesterday's date
    yesterday = today - datetime.timedelta(days=1)

    # Format the dates as strings
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    # Lists of file names for today and yesterday
    today_files = [f'DailyRun/data {today}.csv']  # Add more files as needed
    yesterday_files = [f'DailyRun/data {yesterday}.csv']  # Add more files as needed

    # Lists to store LotNum and rows
    yesterday_lotnum = []
    today_lotnum = []
    yesterday_rows = []
    today_rows = []
    sold_rows = []
    new_unit_rows = []

    #write to csv 
    def writeToCsv(name, array):

        array_name = array    

        with open(name + f' {today}.csv', 'w', newline='') as writer :
            writer = csv.writer(writer, quoting=csv.QUOTE_ALL)
            writer.writerow(['Year','Company','Brand','FloorPlan','Msrp','Discount','StockNumber','UnitType','Location','Dealer','Date'])
        
            for iteam in array_name:
                year = iteam[0]
                company = iteam[1]
                brand = iteam[2]
                floor = iteam[3]
                msrpbase = iteam[4]
                msrpdiscount = iteam[5]
                lotnum = iteam[6]
                category = iteam[7]
                location = iteam[8]
                dealer = iteam[9]
                date = iteam[10]
                writer.writerow([year,company,brand,floor,msrpbase,msrpdiscount,lotnum,category,location,dealer,date])

    def appentToCsv(name,arrayToAppend):

        with open(name, 'a', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            
            for iteam in arrayToAppend:
                year = iteam[0]
                company = iteam[1]
                brand = iteam[2]
                floor = iteam[3]
                msrpbase = iteam[4]
                msrpdiscount = iteam[5]
                lotnum = iteam[6]
                category = iteam[7]
                location = iteam[8]
                dealer = iteam[9]
                date = iteam[10]
                writer.writerow([year,company,brand,floor,msrpbase,msrpdiscount,lotnum,category,location,dealer,date])

    # Function to read LotNum and rows from a CSV file
    def read_lotnum_and_rows(filenames, lotnum_list, row_list, lotnum_index):
        for filename in filenames:
            try:
                with open(filename, 'r', newline='') as file:
                    reader = csv.reader(file)
                    header = next(reader)  # Skip header
                    for row in reader:
                        lotnum_list.append(row[lotnum_index])
                        row_list.append(row)
            except FileNotFoundError:
                print(f"File not found: {filename}")

    # Function to find sold units
    def find_sold_units(yesterday_lotnum, today_lotnum):
        sold = [lot for lot in yesterday_lotnum if lot not in today_lotnum]
        return sold

    # Function to find new units
    def find_new_units(yesterday_lotnum, today_lotnum):
        new_units = [lot for lot in today_lotnum if lot not in yesterday_lotnum]
        return new_units



    # Read LotNum and rows from yesterday's files
    read_lotnum_and_rows(yesterday_files, yesterday_lotnum, yesterday_rows, 6)

    # Read LotNum and rows from today's files
    read_lotnum_and_rows(today_files, today_lotnum, today_rows, 6)

    # Find sold units
    sold_lotnum = find_sold_units(yesterday_lotnum, today_lotnum)

    # Find new units
    new_units_lot = find_new_units(yesterday_lotnum, today_lotnum)

    # Collect rows of sold units
    for lot in sold_lotnum:
        for row in yesterday_rows:
            if row[6] == lot:
                sold_rows.append(row)

    # Collect rows of new units
    for lot in new_units_lot:
        for row in today_rows:
            if row[6] == lot:
                new_unit_rows.append(row)


    appentToCsv('rvMainSold.csv', sold_rows)
    appentToCsv('rvMainNew.csv', new_unit_rows)
    #write file of sold units
   # writeToCsv('soldUnits', sold_rows)
    #write file of new units
   # writeToCsv('newUnits', new_unit_rows)

def boatValidate():

    # Get today's date
    today = datetime.date.today()

    # Calculate yesterday's date
    yesterday = today - datetime.timedelta(days=1)

    # Format the dates as strings
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    # Lists of file names for today and yesterday
    today_files = [f'DailyRun/BoatDaily {today}.csv']  # Add more files as needed
    yesterday_files = [f'DailyRun/BoatDaily {yesterday}.csv']  # Add more files as needed

    # Lists to store LotNum and rows
    yesterday_lotnum = []
    today_lotnum = []
    yesterday_rows = []
    today_rows = []
    sold_rows = []
    new_unit_rows = []

    #write to csv 
    def writeToCsv(name, array):

        array_name = array    

        with open(name + f' {today}.csv', 'w', newline='') as writer :
            writer = csv.writer(writer, quoting=csv.QUOTE_ALL)
            writer.writerow(['Year', 'Company', 'Model','FloorPlan', 'Length','Engine', 'StockNumber','Dealer', 'Location','Msrp','Discount','Date'])
        
            for iteam in array_name:
                year = iteam[0]
                company = iteam[1]
                model = iteam[2]
                floor = iteam[3]
                length = iteam[4]
                engine = iteam[5]
                lotnum = iteam[6]
                dealer = iteam[7]
                location = iteam[8]
                msrpbase = iteam[9]
                msrpdiscount = iteam[10]
                date = iteam[11]
                writer.writerow([year,company,model,floor,length,engine,lotnum,dealer,location,msrpbase,msrpdiscount,date])

    def appentToCsv(name,arrayToAppend):
        array = arrayToAppend

        with open(name,'a',newline='') as writer :
            writer = csv.writer(writer, quoting=csv.QUOTE_ALL)

        for iteam in array:
            if len(iteam) >= 12:  # Ensure there are at least 12 elements
                year = iteam[0]
                company = iteam[1]
                model = iteam[2]
                floor = iteam[3]
                length = iteam[4]
                engine = iteam[5]
                lotnum = iteam[6]
                dealer = iteam[7]
                location = iteam[8]
                msrpbase = iteam[9]
                msrpdiscount = iteam[10]
                date = iteam[11]
                writer.writerow([year, company, model, floor, length, engine, lotnum, dealer, location, msrpbase, msrpdiscount, date])
            else:
                print(f"Row has missing elements and will be skipped: {iteam}")

    # Function to read LotNum and rows from a CSV file
    def read_lotnum_and_rows(filenames, lotnum_list, row_list, lotnum_index):
        for filename in filenames:
            try:
                with open(filename, 'r', newline='') as file:
                    reader = csv.reader(file)
                    header = next(reader)  # Skip header
                    for row in reader:
                        lotnum_list.append(row[lotnum_index])
                        row_list.append(row)
            except FileNotFoundError:
                print(f"File not found: {filename}")

    # Function to find sold units
    def find_sold_units(yesterday_lotnum, today_lotnum):
        sold = [lot for lot in yesterday_lotnum if lot not in today_lotnum]
        return sold

    # Function to find new units
    def find_new_units(yesterday_lotnum, today_lotnum):
        new_units = [lot for lot in today_lotnum if lot not in yesterday_lotnum]
        return new_units



    # Read LotNum and rows from yesterday's files
    read_lotnum_and_rows(yesterday_files, yesterday_lotnum, yesterday_rows, 6)

    # Read LotNum and rows from today's files
    read_lotnum_and_rows(today_files, today_lotnum, today_rows, 6)

    # Find sold units
    sold_lotnum = find_sold_units(yesterday_lotnum, today_lotnum)

    # Find new units
    new_units_lot = find_new_units(yesterday_lotnum, today_lotnum)

    # Collect rows of sold units
    for lot in sold_lotnum:
        for row in yesterday_rows:
            if row[6] == lot:
                sold_rows.append(row)

    # Collect rows of new units
    for lot in new_units_lot:
        for row in today_rows:
            if row[6] == lot:
                new_unit_rows.append(row)


    appentToCsv('boatSoldUnits.csv', sold_rows)
    appentToCsv('boatNewUnits.csv', new_unit_rows)

def rvCreateOneFile():
    today = datetime.date.today()
    seen_lot_numbers = set()
    files = [f'DailyFiles/Campersinn {today}.csv',f'DailyFiles/LazyDays {today}.csv',f'DailyFiles/GeneralRV {today}.csv',f'DailyFiles/Bluecompass RV {today}.csv',f'DailyFiles/Bish {today}.csv',
             f'DailyFiles/Arbutus {today}.csv',f'DailyFiles/Wilkins {today}.csv',f'DailyFiles/RonHoover {today}.csv', f'DailyFiles/RonHoover {today}.csv',f'DailyFiles/Meyers {today}.csv',f'DailyFiles/HWH {today}.csv',f'DailyFiles/Parris {today}.csv',f"DailyFiles/CampingWorld {today}.csv",
             f'DailyFiles/Adventure Motorhomes {today}.csv',f'DailyFiles/Alpinhaus {today}.csv',f'DailyFiles/Bretz {today}.csv',f'DailyFiles/Crestview {today}.csv',f'DailyFiles/Dicks {today}.csv',f'DailyFiles/EvansRV Sales {today}.csv',f'DailyFiles/HappyDaze {today}.csv',f'DailyFiles/Ketelsen {today}.csv',
             f'DailyFiles/LittleDealer {today}.csv',f'DailyFiles/Mikethompson {today}.csv',f'DailyFiles/Pleasureland {today}.csv',f'DailyFiles/Pontiac {today}.csv',f'DailyFiles/Roberson {today}.csv',f'DailyFiles/RvVacation {today}.csv',f'DailyFiles/Stoltzfus {today}.csv',f'DailyFiles/Tomschaeffers {today}.csv',
             f'DailyFiles/TrailerHitch {today}.csv',f'DailyFiles/Wheels {today}.csv',f'DailyFiles/Windish {today}.csv',f'DailyFiles/Boyersales {today}.csv',f'DailyFiles/Markquart {today}.csv',f'DailyFiles/Submmit {today}.csv',f'DailyFiles/Bullyan {today}.csv',f'DailyFiles/Southland {today}.csv',f'DailyFiles/1000Island {today}.csv',
             f'DailyFiles/Steves {today}.csv',f'DailyFiles/Cordelia {today}.csv'
             ]
    count = 0
    for nam1 in files:
        try:
            with open(nam1, newline='') as input_file, \
                    open(f'DailyRun/data {today}.csv', 'a', newline='') as output_file:
                reader = csv.reader(input_file, delimiter=',', quotechar='"')
                writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                if count == 0:
                    writer.writerow(['Year','Company','Brand','FloorPlan','Msrp','Discount','StockNumber','UnitType','Location','Dealer','Date','New/Used'])
                
                first_row = next(reader, None)  # Skip the first row

                for row in reader:
                    lot_num = row[6]  # Assuming LotNum is in the 10th column (index 9)
                    if lot_num in seen_lot_numbers:
                        continue  # Skip this row if the LotNum is already seen
                    
                    seen_lot_numbers.add(lot_num)  # Add the LotNum to the set

                    modified_row = []
                    for i, value in enumerate(row):
                        if i == 9 or i == 10:  # Columns 10 and 11 (index starts from 0)
                            modified_value = value.replace(',', '').replace('$', '')
                            modified_row.append(modified_value)
                        else:
                            modified_row.append(value)
                    writer.writerow(modified_row)
        except FileNotFoundError:
            print(f"{nam1} unable to find")
        count += 1

def boatCreateOneFile():
    today = datetime.date.today()
    seen_lot_numbers = set()
    files = [
            f'DailyFiles/Buckeye {today}.csv',f'DailyFiles/DesmasDons {today}.csv',f'DailyFiles/Futrell Marine {today}.csv',f'DailyFiles/MarineSales {today}.csv',f'DailyFiles/Moose Landing {today}.csv',f'DailyFiles/SeattleBoats {today}.csv',f'DailyFiles/Spicers Boat {today}.csv',
            f'DailyFiles/TimsFord {today}.csv',f'DailyFiles/WakeSide {today}.csv',f'DailyFiles/MontanaBoatCenter {today}.csv',f'DailyFiles/UnionMarine {today}.csv',f'DailyFiles/RevolutionMarine {today}.csv',f'DailyFiles/Valley Marine {today}.csv',f'DailyFiles/Harrison Marine {today}.csv',
            f'DailyFiles/River City {today}.csv',f'DailyFiles/Water World {today}.csv',f'DailyFiles/Hawkeye {today}.csv',f'DailyFiles/Slc Baots {today}.csv',f'DailyFiles/Blm Boats {today}.csv',f'DailyFiles/Mattas Marine {today}.csv',f'DailyFiles/West Cost {today}.csv',
            f'DailyFiles/Action Water {today}.csv',f'DailyFiles/Anderson Power {today}.csv',f'DailyFiles/WMF Watercraft {today}.csv',f'DailyFiles/Westorlando {today}.csv',f'DailyFiles/Wayzata Marine {today}.csv',f'DailyFiles/WaterWorkz Marine {today}.csv',f'DailyFiles/Wateree Marine {today}.csv',
            f'DailyFiles/ShyBeaver {today}.csv',f'DailyFiles/Route1 MotorSports {today}.csv',f'DailyFiles/Plano Marine {today}.csv',f'DailyFiles/Perfect Catch {today}.csv',f'DailyFiles/Paradise Marine {today}.csv',f'DailyFiles/NorthPoint WaterSports {today}.csv',f'DailyFiles/Mountain Marine {today}.csv',
            f'DailyFiles/Marine Specialist {today}.csv',f'DailyFiles/Leadersrpm {today}.csv',f'DailyFiles/Inland Boat {today}.csv',f'DailyFiles/Hillyers {today}.csv',f'DailyFiles/Grandpas Marine {today}.csv',f'DailyFiles/Germaine Marine {today}.csv',f'DailyFiles/Gainesville Marina {today}.csv',
            f'DailyFiles/Funnsun Boats {today}.csv',f'DailyFiles/Deland Motors {today}.csv', f'DailyFiles/Captains choice {today}.csv',f'DailyFiles/Bryans Marine {today}.csv',f'DailyFiles/Brainerd Sports {today}.csv',f'DailyFiles/BoatAndMotor SuperStores {today}.csv',f'DailyFiles/Berkeley {today}.csv',
            f'DailyFiles/Barnes Marine {today}.csv',f'DailyFiles/Augusta Marine {today}.csv',f'DailyFiles/Appleton Boats {today}.csv',f'DailyFiles/Anchorage Yacht {today}.csv'
        ]
    count = 0
    for nam1 in files:
        try:
            with open(nam1, newline='') as input_file, \
                    open(f'DailyRun/BoatDaily {today}.csv', 'a', newline='') as output_file:
                reader = csv.reader(input_file, delimiter=',', quotechar='"')
                writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                if count == 0:
                    writer.writerow(['Year', 'Company', 'Model','FloorPlan', 'Length','Engine', 'StockNumber','Dealer', 'Location','Msrp','Discount','Date'])
                
                first_row = next(reader, None)  # Skip the first row

                for row in reader:
                    lot_num = row[6]  # Assuming LotNum is in the 10th column (index 9)
                    if lot_num in seen_lot_numbers:
                        print(f'Duplicated  {lot_num}')
                        continue  # Skip this row if the LotNum is already seen
                    
                    seen_lot_numbers.add(lot_num)  # Add the LotNum to the set

                    writer.writerow(row)
        except FileNotFoundError:
            print(f"{nam1} unable to find")
        count += 1