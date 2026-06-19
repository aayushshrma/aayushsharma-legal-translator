
import streamlit as st
import tempfile
import time
from pathlib import Path
from converter import convert_to_markdown
from translator import translation_to_english
from app_utils import logger, save_log_to_excel, time_, save_translation_docx


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(page_title="Trआnsलेटr", page_icon="📄", layout="centered")

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .center-text {
        text-align: center;
    }

    div.stButton > button p {
        font-size: 18px !important;
        font-weight: 700;
        height: 28px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.title("About")

    st.write(
        """
        **Trआnsलेटr** is an AI-powered document translation platform
        for Hindi and Punjabi documents. Unlike traditional
        translators that work only with plain text or text-selectable PDFs,
        Trआnsलेटr is designed to translate scanned PDFs and images accurately.

        Supported formats:

        - PDF
        - JPG
        - JPEG
        - PNG

        Built for government records, legal documents,
        land records, certificates, and scanned paperwork.\n
        **Built with ❤️ by Aayush Sharma**
        """
    )

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.markdown('<div class="main-title">Trआnsलेटr</div>', unsafe_allow_html=True)

st.markdown('<div class="center-text">Hindi & Punjabi → English Document Translator</div>', unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------

uploaded_file = st.file_uploader("Upload Document", type=["pdf", "jpg", "jpeg", "png"])

st.write("")

# ---------------------------------------------------------
# TRANSLATE BUTTON
# ---------------------------------------------------------

col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    translate_clicked = st.button(
        "Trआnsलेट",
        width="stretch",
        type="secondary"
    )

if translate_clicked:
    if uploaded_file is None:

        st.warning("Please upload a document.")

    else:

        start_time, d, t = time_()

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            
            tmp.write(uploaded_file.read())
            input_file = tmp.name
            doc_name = f"{Path(uploaded_file.name).stem}_{d.replace("/", "_")}_{t.replace(":", "_")}"

        # -----------------------------------------
        # Progress Bar
        # -----------------------------------------

        progress_bar = st.progress(0)
        status = st.empty()
        time.sleep(0.5)
        progress_bar.progress(15)

        status.text("Reading Data...")
        markdown_text, stats_ocr = convert_to_markdown(doc_url=input_file, doc_name=doc_name, pg_range="")
        progress_bar.progress(50)

        status.text("Translating document...")
        output_file = f"output_translation/{doc_name}_translated.md"
        translated_text, stats_trans = translation_to_english(markdown_text=markdown_text, output_file=output_file)
        progress_bar.progress(80)

        status.text("Generating DOCX...")
        output_file_docx = f"output_docx/{doc_name}_translated.docx"
        save_translation_docx(md_text=translated_text, output_file=output_file_docx)
        progress_bar.progress(90)

        status.text("Generating Stats...")
        time.sleep(0.5)
        log_dict = logger()
        log_dict["DATE"] = d
        log_dict["TIME"] = t
        log_dict["PROCESS"] = "OCR + Translation"
        log_dict["FILENAME"] = doc_name
        log_dict["NO. OF PAGES"] = stats_ocr["PAGES"]
        log_dict["DURATION (OCR)"] = stats_ocr["DURATION"]
        log_dict["COST (OCR)"] = stats_ocr["COST"]
        log_dict["OCR_SCORE"] = stats_ocr["OCR_SCORE"]
        log_dict["DURATION (TRANSLATION)"] = stats_trans["DURATION"]
        log_dict["COST (TRANSLATION)"] = stats_trans["COST"]
        save_log_to_excel(log_dict=log_dict)
        total_cost = (float(stats_ocr["COST"]) + float(stats_trans["COST"]))
        revenue = total_cost * 5
        log_dict["TOTAL COST"] = total_cost
        log_dict["REVENUE (INR)"] = revenue


        translated_file_path = output_file_docx
        progress_bar.progress(100)
        status.text("Completed")

        end_time, _, _ = time_()
        duration = (end_time - start_time).total_seconds()/60

        st.success("Translation completed successfully!")
        st.write("")

        # -------------------------------------------------
        # DOWNLOAD BUTTON
        # -------------------------------------------------

        if Path(translated_file_path).exists():

            with open(translated_file_path, "rb") as file:

                st.download_button(label="Download Translation", data=file,
                    file_name=Path(translated_file_path).name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        # -------------------------------------------------
        # STATS
        # -------------------------------------------------

        st.write("")
        st.subheader("Translation Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Processing Time", f"{duration:.2f} mins")

        with col2:
            st.metric("Cost", f"INR {revenue:.2f}")
