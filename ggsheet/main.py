from db.db_mgmt import import_csv_to_postgresql
from gg_sheet.ggsheet import download_gg_sheet
from configparser import ConfigParser

config = ConfigParser()
config.read("gg_sheet/credential.ini")

csv_file_path = "ggsheet/files/data.csv"


def main():
    # download_gg_sheet()
    import_csv_to_postgresql(csv_file_path, table_name="test_gg_sheet")


if __name__ == "__main__":
    main()
