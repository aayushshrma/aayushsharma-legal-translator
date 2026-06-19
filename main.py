from converter import convert_to_markdown
from translator import translation_to_english
from utils import select_file, select_pipeline_action, save_translation_docx, logger, save_log_to_excel
from pathlib import Path


OUTPUT_DIR = "output_translation"
OUTPUT_DIR_DOCX = "output_docx"
MODEL = "gpt-5.5"

def main():

    stats_ocr, stats_trans = None, None
    log_dict = logger()

    action = select_pipeline_action()
    if action is None:
        print("NO ACTION DEFINED")
        exit()

    elif action == "OCR Conversion":
        print("RUNNING OCR CONVERSION")
        doc_url, doc_name = select_file(allowed_filetypes=[("Supported Files", "*.pdf *.jpg *.jpeg *.png")])
        if doc_url is None:
            print("NO FILE SELECTED!")
            exit()
        markdown_text, stats_ocr = convert_to_markdown(doc_url=doc_url, doc_name=doc_name, pg_range="")

    elif action == "Translation":
        print("RUNNING TRANSLATION")
        doc_url, doc_name = select_file(allowed_filetypes=[("Supported Files", "*.md")])
        markdown_text = Path(doc_url).read_text(encoding="utf-8")
        output_file = f"{OUTPUT_DIR}/{doc_name}_translated.md"
        translated_text, stats_trans = translation_to_english(markdown_text=markdown_text, output_file=output_file)
        output_file_docx = f"{OUTPUT_DIR_DOCX}/{doc_name}_translated.docx"
        save_translation_docx(md_text=translated_text, output_file=output_file_docx)

    elif action == "OCR + Translation":
        print("RUNNING FULL PIPELINE")
        doc_url, doc_name = select_file(allowed_filetypes=[("Supported Files", "*.pdf *.jpg *.jpeg *.png")])
        if doc_url is None:
            print("NO FILE SELECTED!")
            exit()
        markdown_text, stats_ocr = convert_to_markdown(doc_url=doc_url, doc_name=doc_name, pg_range="")
        output_file = f"{OUTPUT_DIR}/{doc_name}_translated.md"
        translated_text, stats_trans = translation_to_english(markdown_text=markdown_text, output_file=output_file)
        output_file_docx = f"{OUTPUT_DIR_DOCX}/{doc_name}_translated.docx"
        save_translation_docx(md_text=translated_text, output_file=output_file_docx)
    
    log_dict["PROCESS"] = action
    log_dict["FILENAME"] = doc_name

    if stats_ocr:
        log_dict["NO. OF PAGES"] = stats_ocr["PAGES"]
        log_dict["DURATION (OCR)"] = stats_ocr["DURATION"]
        log_dict["COST (OCR)"] = stats_ocr["COST"]
        log_dict["OCR_SCORE"] = stats_ocr["OCR_SCORE"]
    
    if stats_trans:
        log_dict["DURATION (TRANSLATION)"] = stats_trans["DURATION"]
        log_dict["COST (TRANSLATION)"] = stats_trans["COST"]
    
    save_log_to_excel(log_dict=log_dict)


if __name__ == "__main__":
    main()