from pathlib import Path
from openai import OpenAI
import os
import streamlit as st
from utils import time_


def translation_to_english(markdown_text, output_file, model_name="gpt-5.5"):
    stats = {}
    start_time_, _, _ = time_()
    
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        api_key = os.environ["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)

    # ------------------------------------------------------------------
    # Translation Prompt
    # ------------------------------------------------------------------

    SYSTEM_PROMPT = """
    You are a professional legal document translator.

    Translate Hindi or Punjabi documents into English.

    Requirements:

    1. Preserve meaning exactly.
    2. Preserve all Markdown formatting.
    3. Preserve headings, tables, lists and numbering.
    4. Do NOT summarize.
    5. Do NOT omit substantive document content.
    6. Do NOT explain.
    7. Translate literally where possible.
    8. Return only the translated Markdown.

    Page Handling Rules:
    9. The document is divided into pages numbered from 0 onwards.
    10. Preserve and translate page headers, letterheads, and document-identifying information on page 0.
    11. For all pages after page 0, Omit repeated headers, letterheads, page numbers, and other repeated page-level boilerplate.
    12. Text may continue across page boundaries. Translate the document as a continuous document and preserve its logical flow.
    13. Remove page break markers, page separator markers, and pagination artifacts from the translated output.
    """

    # ------------------------------------------------------------------
    # Translation
    # ------------------------------------------------------------------

    print("TRANSLATING DOCUMENT...")

    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": markdown_text,
            },
        ],
    )

    translated_markdown = response.output_text
    usage = response.usage

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    Path(output_file).write_text(translated_markdown, encoding="utf-8")

    print(f"Translation saved to: {output_file}")
    end_time_, _, _ = time_()
    duration = (end_time_ - start_time_).total_seconds()/60

    # ------------------------------------------------------------------
    # Usage
    # ------------------------------------------------------------------

    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    cost = (
        (input_tokens / 10000) * 5
        +
        (output_tokens / 10000) * 30
        )
    
    stats["DURATION"] = f"{duration:.2f}"
    stats["COST"] = cost

    return translated_markdown, stats
