import os
import re
from app_utils import time_
import streamlit as st
from datalab_sdk import DatalabClient, ConvertOptions


# Clean Markdown
def clean_markdown(text: str) -> str:
    # Remove markdown image references
    text = re.sub(r'!\[.*?\]\(.*?\)','',text)

    # Collapse excessive blank lines
    text = re.sub(r'\n{3,}','\n\n',text)

    return text


def convert_to_markdown(doc_url, doc_name, pg_range: str):
        stats = {}
        start_time_, _, _ = time_()
        print("CONVERTING...")

        try:
               api_key = st.secrets["DATALAB_API_KEY"]
        except:
               api_key = os.environ["DATALAB_API_KEY"]
        client = DatalabClient(api_key=api_key)

        # Convert a document to markdown
        options = ConvertOptions(mode="accurate", page_range=pg_range, paginate=True,
                                disable_image_extraction=True, disable_image_captions=True, skip_cache=True,
                                additional_config={"keep_pageheader_in_output":False,
                                                   "keep_pagefooter_in_output":False})

        result = client.convert(doc_url, options=options)

        print("CLEANING MARKDOWN")
        markdown_text = result.markdown
        markdown_text = clean_markdown(markdown_text)

        with open(f"output_ocr/{doc_name}.md", "w", encoding="utf-8") as file:
                file.write(markdown_text)

        print("CONVERTED TO MARKDOWN SUCCESSFULLY!")
        end_time_, _, _ = time_()
        duration = (end_time_ - start_time_).total_seconds()/60

        # Stats
        stats["DURATION"] = f"{duration:.2f}"
        stats["OCR_SCORE"] = result.parse_quality_score
        stats["COST"] = result.cost_breakdown['final_cost_cents']
        stats["PAGES"] = result.page_count


        return markdown_text, stats

