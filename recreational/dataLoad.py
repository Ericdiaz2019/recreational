from pymongo import MongoClient
import csv
import datetime


def load_data_daily_pull(csv_file, name_collection, delete):
    #grabtoday
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    ### dataBase Information ###
    data_base_url = 'mongodb+srv://ericjesusdiaz:J9gflBfEgZVAvw6q@recreational-main.0luff86.mongodb.net/?retryWrites=true&w=majority&appName=recreational-main'
    db_collection = ['DailyPull','DailyNew','DailySold','AllTimeSold','AllTimeNew','DailyBoatPull','AllTimeBoatSold','AllTimeBoatNew']
    cluster = MongoClient(data_base_url)
    db = cluster["recreational-main"]


    # Establish MongoDB connection
    collection = db[name_collection]
    
    if delete == 'Yes':
        delete_result = collection.delete_many({})
        print(f"Deleted {delete_result.deleted_count} documents from the collection")
    else:
        print('No deleted document')
    
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            # Set LotNum as the _id field
            row['_id'] = row['StockNumber']
            data.append(row)
        
        # Insert all data into MongoDB
        if data:
            insert_result = collection.insert_many(data)
            print(f"Inserted {len(insert_result.inserted_ids)} documents")
    



def load_data_daily_pull_boat(csv_file, name_collection, delete):
    #grabtoday
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    ### dataBase Information ###
    data_base_url = 'mongodb+srv://ericjesusdiaz:J9gflBfEgZVAvw6q@recreational-main.0luff86.mongodb.net/?retryWrites=true&w=majority&appName=recreational-main'
    db_collection = ['DailyPull','DailyNew','DailySold','AllTimeSold','AllTimeNew','DailyBoatPull','AllTimeBoatSold','AllTimeBoatNew']
    cluster = MongoClient(data_base_url)
    db = cluster["recreational-main"]


    # Establish MongoDB connection
    collection = db[name_collection]
    
    if delete == 'Yes':
        delete_result = collection.delete_many({})
        print(f"Deleted {delete_result.deleted_count} documents from the collection")
    else:
        print('No deleted document')
    
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            # Set LotNum as the _id field
            row['_id'] = row['StockNumber']
            data.append(row)
        
        # Insert all data into MongoDB
        if data:
            insert_result = collection.insert_many(data)
            print(f"Inserted {len(insert_result.inserted_ids)} documents")