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


