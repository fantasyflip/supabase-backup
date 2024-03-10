# Supabase Database Backup Script

## Overview
This Python script is designed to automate the backup process for Supabase databases using a grandfather-father-son backup scheme. By running this script daily through a cronjob, it ensures the creation of regular backups and organizes them into daily, weekly, and monthly folders. The backup files are stored in the specified root path, and the script provides detailed logging for monitoring the backup process.

## Features
- **Grandfather-Father-Son Backup Scheme:** The script organizes backups into daily, weekly, and monthly folders to maintain a historical backup record.
- **Flexible Configuration:** Easily configure the script by adding or modifying database details in the `databases` array, including database name, user, Supabase subdomain ID, password, and dump file name.
- **Automatic Backup:** The script automatically pulls database dumps, organizes them into appropriate folders, and maintains the specified number of backups for each timeframe (daily, weekly, and monthly).
- **Logging:** Detailed logging is implemented, recording each step of the backup process. The log file is located at `/mnt/supabase-backup/supabase-backup.log` by default.

## Prerequisites
- Ensure Python 3 is installed on your system.
- Set up a cronjob to run the script daily.

## Configuration
1. Open the script and navigate to the `databases` array.
2. Add your Supabase databases with the required details, such as name, user, Supabase subdomain ID, password, and dump file name.

```python
databases = [
    {
        "name": "Database-A",
        "user": "postgres",
        "id": "abcdefg",
        "password": "xxxxxxxx",
        "dumpName": "db-a-dump.sql"
    },
    # Add more databases as needed
]
```

## Usage

1. Make the script executable:

```bash
chmod +x /path/to/backup_script.py
```

2. Set up a cronjob to run the script daily. Example:

```bash
0 0 * * * /path/to/backup_script.py
```

This example runs the script every day at midnight.

## Monitoring
Check the log file at `/mnt/supabase-backup/supabase-backup.log` for detailed information on each backup process. Monitor this log to ensure the script is running successfully and backups are being created and organized accordingly.

**Note:** Make sure to secure the script and log files appropriately to prevent unauthorized access.