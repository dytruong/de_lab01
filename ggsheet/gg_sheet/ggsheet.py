import gspread
from configparser import ConfigParser
import csv
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")


def config(file_name="./ggsheet/gg_sheet/credential.ini", section="default"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(file_name)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {file_name} file")

    return db


def download_gg_sheet():
    # Connect to Google Sheets API
    params = config()
    gc = gspread.service_account(filename=params["credentials_file"])
    sh = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1yx2hG2wfmWytpxSrljE3rYrtIHD0vcm56G8bHbWn4Jg/edit?usp=sharing"
    )
    worksheet = sh.sheet1

    # Fetch data from the Google Sheet
    data = worksheet.get_all_values()
    # Export updates to CSV
    csv_file_path = params["csv_file_path"]
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
