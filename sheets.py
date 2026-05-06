import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_SERVICE_ACCOUNT_JSON, SPREADSHEET_ID


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_sheet(name):
    creds = Credentials.from_service_account_info(
        GOOGLE_SERVICE_ACCOUNT_JSON,
        scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).worksheet(name)


def get_records(sheet_name):
    sheet = get_sheet(sheet_name)
    return sheet.get_all_records()


def append_rows(sheet_name, rows):
    sheet = get_sheet(sheet_name)
    if rows:
        sheet.append_rows(rows, value_input_option="USER_ENTERED")


def get_existing_review_ids(sheet_name):
    sheet = get_sheet(sheet_name)

    values = sheet.col_values(9)  # 리뷰 ID 컬럼 (I열)

    # 헤더 제외
    return set(v.strip() for v in values[1:] if v.strip())
