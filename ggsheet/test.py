import gspread
import csv
import psycopg2
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)s - %(message)s"
)

# Google Sheets API credentials
# Make sure to set up authentication and obtain the credentials file
credentials_file = "cred/gg-sheet-cred.json"
spreadsheet_id = '1czr2XWfOODB9eAmDDkMj8TfXBcFWI2wx'


# File path for the CSV export
csv_file_path = 'data.csv'

# Connect to Google Sheets API
gc = gspread.service_account(filename=credentials_file)
logging.debug(gc)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1yx2hG2wfmWytpxSrljE3rYrtIHD0vcm56G8bHbWn4Jg/edit?usp=sharing")
worksheet = sh.sheet1  # Assuming the data is in the first sheet

# Fetch data from the Google Sheet
data = worksheet.get_all_values()
logging.debug(data)

# Load previous data from PostgreSQL or file
# Perform comparison to identify updates

# Export updates to CSV
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)


# Create a table in PostgreSQL that matches the structure of the data
create_table_query = """
    CREATE TABLE cp_specs (
        No INT,
        Components VARCHAR(255),
        Description VARCHAR(255),
        LinkDescription VARCHAR(255),
        Quantity INT,
        Price DECIMAL(10, 2)
    );

"""
stt = cursor.execute(create_table_query)
logging.debug(stt)

# Import data from CSV into PostgreSQL
copy_query = """
    COPY cp_specs FROM %s WITH CSV HEADER;
"""
cursor.execute(copy_query, (csv_file_path,))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()