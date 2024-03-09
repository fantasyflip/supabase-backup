#!/usr/bin/python3
import os 
from datetime import datetime, date
import logging

# array of databases and their credentials
rootPath = "/mnt/supabase-backup/"
logPath = "/mnt/supabase-backup/supabase-backup.log"
databases = [
    {
        "name": "Database-A",
        "user": "postgres", # typically postgres
        "id": "abcdefg", # supabase subdomain name
        "password":"xxxxxxxx", # postgres password
        "dumpName": "db-a-dump.sql" # name of the dump
    },
]

# pull db dumps of every database

logging.basicConfig(filename=logPath, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', )

for i in databases:
    path = f"{rootPath}{i['name']}"
    logging.info(f"Dumping database {i['name']} to {path}")
    if not os.path.isdir(path):
        logging.info(f"Creating directory {path}")
        os.makedirs(path)

    os.chdir(path)
    # yyyy-mm-dd_dumpName.sql
    dumpName = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{i['dumpName']}"
    os.system(f"pg_dump 'postgres://{i['user']}.{i['id']}:{i['password']}@aws-0-eu-central-1.pooler.supabase.com:5432/postgres' > {dumpName}")

# verify db dump is downloaded

    if os.path.isfile(dumpName):
        logging.info(f"Database {i['name']} has been successfully dumped.")
    else:
        logging.error(f"Database {i['name']} has failed to dump.")
    
   # if its the first date of the month, copy dump into 'monthly' folder
    if date.today().day == 1:
        monthlyPath = f"{path}/monthly"
        if not os.path.isdir(monthlyPath):
            os.makedirs(monthlyPath)
        # copy dump into monthly folder
        os.system(f"cp {dumpName} {monthlyPath}/{dumpName}")
        
        logging.info(f"Database {i['name']} has been moved to {monthlyPath}/{dumpName}")
        
        # delete oldest dump if theres more than 6 dumps
        dumps = sorted(os.listdir(monthlyPath), key=lambda x: os.path.getctime(os.path.join(monthlyPath, x)))
                    
        while len(dumps) > 6:
            oldestDump = dumps.pop(0)  # Remove and return the first item, which is the oldest
            os.remove(os.path.join(monthlyPath, oldestDump))
            logging.info(f"Database {i['name']} has deleted the oldest dump {oldestDump}")
        
        if not dumps:
            logging.info(f"Database {i['name']} has not deleted the oldest dump as there are less than 6 dumps.")
    
    # if its the first day of the week, move dump into 'weekly' folder
    if date.today().weekday() == 0:
        weeklyPath = f"{path}/weekly"
        if not os.path.isdir(weeklyPath):
            os.makedirs(weeklyPath)
        # copy dump into weekly folder
        os.system(f"cp {dumpName} {weeklyPath}/{dumpName}")
        logging.info(f"Database {i['name']} has been moved to {weeklyPath}/{dumpName}")
        
        # delete oldest dump if theres more than 4 dumps
        dumps = sorted(os.listdir(weeklyPath), key=lambda x: os.path.getctime(os.path.join(weeklyPath, x)))
            
        while len(dumps) > 4:
            oldestDump = dumps.pop(0)  # Remove and return the first item, which is the oldest
            os.remove(os.path.join(weeklyPath, oldestDump))
            logging.info(f"Database {i['name']} has deleted the oldest dump {oldestDump}")
        
        if not dumps:
            logging.info(f"Database {i['name']} has not deleted the oldest dump as there are less than 4 dumps.")
    
    # copy dump into daily folder
    dailyPath = f"{path}/daily"
    if not os.path.isdir(dailyPath):
        os.makedirs(dailyPath)
    # copy dump into daily folder
    os.system(f"cp {dumpName} {dailyPath}/{dumpName}")
    logging.info(f"Database {i['name']} has been moved to {dailyPath}/{dumpName}")

    # delete oldest dump if theres more than 7 dumps
    dumps = sorted(os.listdir(dailyPath), key=lambda x: os.path.getctime(os.path.join(dailyPath, x)))
    
    while len(dumps) > 7:
        oldestDump = dumps.pop(0)  # Remove and return the first item, which is the oldest
        os.remove(os.path.join(dailyPath, oldestDump))
        logging.info(f"Database {i['name']} has deleted the oldest dump {oldestDump}")
    
    if not dumps:
        logging.info(f"Database {i['name']} has not deleted the oldest dump as there are less than 7 dumps.")
    
    logging.info(f"Database {i['name']} has been successfully backed up.")
    
    # remove dump from root path
    os.remove(dumpName)
    logging.info(f"Database {i['name']} has been removed from the root path.")
    
    #log script end
    logging.info("-------------------------------------------------")

    