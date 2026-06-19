from tkinter import Tk, filedialog
from pathlib import Path
from typing import List, Tuple, Dict
from tkinter import Toplevel, Button, messagebox
import pypandoc
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd


def select_file(allowed_filetypes: List[Tuple[str, str]]):
    root = Tk()
    root.withdraw()

    filepath = filedialog.askopenfilename(
        title="Select a file",
        filetypes=allowed_filetypes
    )

    root.destroy()

    if not filepath:
        return None, None

    filename = Path(filepath).stem

    return filepath, filename


def select_pipeline_action() -> str | None:
    """
    Returns one of:
        "run OCR conversion"
        "run translation"
        "run full pipeline"

    Returns None if the window is closed.
    """

    root = Tk()
    root.withdraw()

    result = None

    def choose(option: str):
        nonlocal result
        result = option
        dialog.destroy()

    dialog = Toplevel(root)
    dialog.title("Select Action")
    dialog.geometry("300x180")
    dialog.resizable(False, False)

    Button(
        dialog,
        text="Run OCR Conversion",
        width=25,
        command=lambda: choose("OCR Conversion")
    ).pack(pady=10)

    Button(
        dialog,
        text="Run Translation",
        width=25,
        command=lambda: choose("Translation")
    ).pack(pady=10)

    Button(
        dialog,
        text="Run Full Pipeline",
        width=25,
        command=lambda: choose("OCR + Translation")
    ).pack(pady=10)

    dialog.grab_set()
    root.wait_window(dialog)

    root.destroy()

    return result


def ask_convert_to_docx():
    result = messagebox.askquestion(title="Convert to .docx?", message="Do you want to convert .md to .docx?")
    return result


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