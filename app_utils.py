from pathlib import Path
import pypandoc
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

def save_translation_docx(md_text: str, output_file: str):

    pypandoc.convert_text(
        md_text,
        to="docx",
        format="md",
        outputfile=output_file
        )
    print("TRANSLATION SAVED AS .docx")


def time_():
    ist_now = datetime.now(ZoneInfo("Asia/Kolkata"))
    current_date = ist_now.strftime("%d/%m/%y")
    current_time = ist_now.strftime("%H:%M:%S")

    return ist_now, current_date, current_time


def logger():
    _, d, t = time_()
    log_dict = {"DATE":d, "TIME":t, "FILENAME":"", "PROCESS": "", "NO. OF PAGES":"",
                "DURATION (OCR)":"", "COST (OCR)": "", "OCR_SCORE":"", "DURATION (TRANSLATION)":"",
                "COST (TRANSLATION)":"", "TOTAL COST":"", "REVENUE (INR)":"", "SUCCESS":"TRUE", "ERROR":""}
    
    return log_dict


from pathlib import Path
import pandas as pd


def save_log_to_excel(log_dict: dict, excel_file: str = "logs/logs.xlsx"):

    excel_path = Path(excel_file)

    new_row = pd.DataFrame([log_dict])

    if excel_path.exists():

        existing_df = pd.read_excel(excel_file)
        df = pd.concat([existing_df, new_row], ignore_index=True)

    else:

        df = new_row
    df.to_excel(excel_file, index=False)


def save_log_to_sheet(log_dict: dict):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
    client = gspread.authorize(creds)

    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1hitGMr5kAdGaY8kowYNYAT4q1GB1CpPvuwV3gYm5DME/edit?usp=sharing").sheet1

    sheet.append_row(list(log_dict.values()))