import csv
import datetime

def validate():

    # Get today's date
    today = datetime.date.today()

    # Calculate yesterday's date
    yesterday = today - datetime.timedelta(days=1)

    # Format the dates as strings
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    # Lists of file names for today and yesterday
    today_files = [f'data {today}.csv']  # Add more files as needed
    yesterday_files = [f'data {yesterday}.csv']  # Add more files as needed

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
            writer.writerow(['Year', 'Company', 'Brand', 'Model', 'FloorPlan', 'Date',
                                'Dealer', 'Category', 'Location', 'LotNum', 'MSRP', 'Discount Price'])
        
            for iteam in array_name:
                year = iteam[0]
                company = iteam[1]
                brand = iteam[2]
                model = iteam[3]
                floor = iteam[4]
                date = iteam[5]
                dealer = iteam[6]
                category = iteam[7]
                location = iteam[8]
                lotnum = iteam[9]
                msrpbase = iteam[10]
                msrpdiscount = iteam[11]
                writer.writerow([year,company,brand,model,floor,date,dealer,category,location,lotnum,msrpbase,msrpdiscount])

    def appentToCsv(name,arrayToAppend):
        array = arrayToAppend

        with open(name,'a',newline='') as writer :
            writer = csv.writer(writer, quoting=csv.QUOTE_ALL)

            for iteam in array:
                year = iteam[0]
                company = iteam[1]
                brand = iteam[2]
                model = iteam[3]
                floor = iteam[4]
                date = iteam[5]
                dealer = iteam[6]
                category = iteam[7]
                location = iteam[8]
                lotnum = iteam[9]
                msrpbase = iteam[10]
                msrpdiscount = iteam[11]
                writer.writerow([year,company,brand,model,floor,date,dealer,category,location,lotnum,msrpbase,msrpdiscount])

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
    read_lotnum_and_rows(yesterday_files, yesterday_lotnum, yesterday_rows, 9)

    # Read LotNum and rows from today's files
    read_lotnum_and_rows(today_files, today_lotnum, today_rows, 9)

    # Find sold units
    sold_lotnum = find_sold_units(yesterday_lotnum, today_lotnum)

    # Find new units
    new_units_lot = find_new_units(yesterday_lotnum, today_lotnum)

    # Collect rows of sold units
    for lot in sold_lotnum:
        for row in yesterday_rows:
            if row[9] == lot:
                sold_rows.append(row)

    # Collect rows of new units
    for lot in new_units_lot:
        for row in today_rows:
            if row[9] == lot:
                new_unit_rows.append(row)

    #write file of sold units
    writeToCsv('soldUnits', sold_rows)
    #write file of new units
    writeToCsv('newUnits', new_unit_rows)
    #append files of sold units to main file
    appentToCsv('allTimeSold.csv',sold_rows)
    #append files of new units to main file
    appentToCsv('allTimeNew.csv',new_unit_rows)

def rvCreateOneFile():
    today = datetime.date.today()
    seen_lot_numbers = set()
    files = [f'DailyFiles/CampingWorld {today}.csv',f'DailyFiles/Campersinn {today}.csv',f'DailyFiles/LazyDays {today}.csv',f'DailyFiles/GeneralRV {today}.csv',f'DailyFiles/Bluecompass RV {today}.csv',f'DailyFiles/Bish {today}.csv',
             f'DailyFiles/Arbutus {today}.csv',f'DailyFiles/Wilkins {today}.csv',f'Daily Dealer Runs/RonHoover RV {today}.csv', f'DailyFiles/RonHoover {today}.csv',f'DailyFiles/Meyers {today}.csv',f'DailyFiles/HWH {today}.csv',f'DailyFiles/Parris {today}.csv']
    count = 0
    for nam1 in files:
        try:
            with open(nam1, newline='') as input_file, \
                    open(f'DailyRun/data {today}.csv', 'a', newline='') as output_file:
                reader = csv.reader(input_file, delimiter=',', quotechar='"')
                writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                if count == 0:
                    writer.writerow(['Year','Company','Brand','FloorPlan','Msrp','Discount','Stock-Number','Unit Type','Location','Dealer','Date','New/Used'])
                
                first_row = next(reader, None)  # Skip the first row

                for row in reader:
                    lot_num = row[9]  # Assuming LotNum is in the 10th column (index 9)
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
    files = [f'DailyFiles/Buckeye {today}.csv',f'DailyFiles/DesmasDons {today}.csv',f'DailyFiles/Futrell Marine {today}.csv',f'DailyFiles/MarineSales {today}.csv',f'DailyFiles/Moose Landing {today}.csv',f'DailyFiles/SeattleBoats {today}.csv',f'DailyFiles/Spicers Boat {today}.csv',
             f'DailyFiles/TimsFord {today}.csv',f'DailyFiles/WakeSide {today}.csv']
    count = 0
    for nam1 in files:
        try:
            with open(nam1, newline='') as input_file, \
                    open(f'DailyRun/BoatDaily {today}.csv', 'a', newline='') as output_file:
                reader = csv.reader(input_file, delimiter=',', quotechar='"')
                writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                if count == 0:
                    writer.writerow(['Year', 'Company', 'Model','FloorPlan', 'Length','Engine', 'Stock Number','Dealer', 'Location','MSRP','DISCOUNT','Date'])
                
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