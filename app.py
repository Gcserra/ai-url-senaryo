import os
import requests
import unicodedata
from bs4 import BeautifulSoup
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from fpdf import FPDF
from PIL import Image
import pytesseract

# ------------------------------------------------------------
# Session‑state helpers
# ------------------------------------------------------------
# Keep generated / edited scenario text in memory so it survives
# the implicit rerun that Streamlit triggers when the user presses
# a download button or interacts with widgets.
# ------------------------------------------------------------
if "scenario_text" not in st.session_state:
    st.session_state["scenario_text"] = ""

# ------------------------------------------------------------
# Environment & API client setup
# ------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------

def remove_accents(text: str) -> str:
    """Strip Turkish characters so FPDF doesn’t complain."""
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

# ------------------------------------------------------------
# 🌍  UI language toggle & static text
# ------------------------------------------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("## 🌐 PathCase AI")
with col2:
    language = st.selectbox("🌐", ["Türkçe", "English"], label_visibility="collapsed")

lang_is_tr = language == "Türkçe"

texts = {
    "title": "🌐 PathCase AI",
    "description": "Bir web sitesi URL’si girin veya ekran görüntüsü yükleyin, içerik analiz edilsin ve yapay zeka size test senaryosu oluştursun." if lang_is_tr else "Enter a website URL or upload a screenshot, let AI analyze it and generate test scenarios.",
    "url_input": "🔗 Web sitesi URL’si girin:" if lang_is_tr else "🔗 Enter website URL:",
    "upload_image": "🖼️ Alternatif olarak bir ekran görüntüsü yükleyin:" if lang_is_tr else "🖼️ Alternatively, upload a screenshot:",
    "url_warning": "Lütfen geçerli bir URL girin veya ekran görüntüsü yükleyin." if lang_is_tr else "Please enter a valid URL or upload a screenshot.",
    "double_input_warning": "Lütfen URL veya ekran görüntüsü seçeneklerinden yalnızca birini kullanın." if lang_is_tr else "Please use either the URL or screenshot option, not both.",
    "img_count_warning": "Lütfen 3 ile 5 arasında ekran görüntüsü yükleyin." if lang_is_tr else "Please upload between 3 and 5 screenshots.",
    "test_type": "🧪 Test Senaryo Türü:" if lang_is_tr else "🧪 Test Scenario Type:",
    "page_type": "🔩 Sayfa Tipini Seçin:" if lang_is_tr else "🔩 Select Page Type:",
    "scenario_count": "🧬 Üretilecek senaryo sayısı:" if lang_is_tr else "🧬 Number of scenarios to generate:",
    "generate": "🚀 Senaryo Üret" if lang_is_tr else "🚀 Generate Scenario",
    "analysis_rate": "📊 Sayfa analiz başarı oranı: %{rate}" if lang_is_tr else "📊 Page analysis success rate: %{rate}",
    "edit_label": "📝 Senaryoyu Düzenleyin:" if lang_is_tr else "📝 Edit the Scenario:",
    "download_label": "### 📅 Senaryoyu indir:" if lang_is_tr else "### 📅 Download the scenario:",
    "download_txt": "📄 .txt olarak indir" if lang_is_tr else "📄 Download as .txt",
    "download_pdf": "🦾 .pdf olarak indir" if lang_is_tr else "🦾 Download as .pdf",
    "error_msg": "Bir hata oluştu: " if lang_is_tr else "An error occurred: ",
}

def _(key: str) -> str:
    return texts.get(key, key)

# ------------------------------------------------------------
# Page description
# ------------------------------------------------------------
st.markdown(texts["description"])

# ------------------------------------------------------------
# Inputs
# ------------------------------------------------------------
url = st.text_input(_("url_input"), placeholder="https://ornek.com/sayfa")
uploaded_files = st.file_uploader(_("upload_image"), type=["png", "jpg", "jpeg"], accept_multiple_files=True)

col1, col2 = st.columns(2)
with col1:
    test_type = st.radio(_("test_type"), ["Tümü", "Pozitif", "Negatif"] if lang_is_tr else ["All", "Positive", "Negative"])
with col2:
    page_options = (
        [
            "Genel",
            "Giriş / Login",
            "Kayıt / Sign‑up",
            "İlan Sayfası",
            "Dashboard",
            "Arama Sayfası",
            "E‑Ticaret Ürün Sayfası",
        ]
        if lang_is_tr
        else [
            "General",
            "Login",
            "Sign‑up",
            "Job Listing Page",
            "Dashboard",
            "Search Page",
            "E‑Commerce Product Page",
        ]
    )
    page_type = st.selectbox(_("page_type"), page_options)

scenario_count = st.slider(_("scenario_count"), min_value=5, max_value=100, value=20, step=5)

# ------------------------------------------------------------
# Generate button handler
# ------------------------------------------------------------
if st.button(_("generate")):
    try:
        # --- Validation ---
        if url.strip() and uploaded_files:
            st.warning(texts["double_input_warning"])
            st.stop()

        if not url.strip() and not uploaded_files:
            st.warning(texts["url_warning"])
            st.stop()

        if uploaded_files and not (3 <= len(uploaded_files) <= 5):
            st.warning(texts["img_count_warning"])
            st.stop()

        with st.spinner("Sayfa analiz ediliyor..." if lang_is_tr else "Analyzing page..."):
            # --- Extract text from either screenshots or URL ---
            if uploaded_files:
                image_texts = []
                for file in uploaded_files:
                    image = Image.open(file)
                    text = pytesseract.image_to_string(image, lang="eng+tur")
                    image_texts.append(text)
                raw_text = "\n".join(image_texts)
            else:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                raw_text = soup.get_text()

            cleaned = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
            input_text = cleaned[:3000]

            # --- Fake analysis % indicator ---
            plen = len(cleaned)
            if plen < 300:
                percent = 10
            elif plen < 1000:
                percent = 40
            elif plen < 2000:
                percent = 70
            else:
                percent = 100
            st.info(_("analysis_rate").format(rate=percent))

            # --- Prompt build & OpenAI call ---
            from prompt_templates import build_prompt  # noqa: import‑placeholder

            prompt = build_prompt(lang_is_tr, scenario_count, page_type, test_type, input_text)

            estimated_tokens = scenario_count * 90
            max_token_limit = min(estimated_tokens, 3800)

            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",  # TODO: make this configurable
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=max_token_limit,
            )

            result = response.choices[0].message.content
            st.session_state["scenario_text"] = result  # 🔑 persist!
            st.success("✅ Test senaryosu oluşturuldu!")
    except Exception as exc:
        st.error(f"{texts['error_msg']}{exc}")

# ------------------------------------------------------------
# Scenario display & download section (shown if we have text)
# ------------------------------------------------------------
if st.session_state["scenario_text"]:
    edited_result = st.text_area(
        texts["edit_label"],
        value=st.session_state["scenario_text"],
        key="scenario_text_box",
        height=400,
    )
    # Keep any edits between reruns
    st.session_state["scenario_text"] = edited_result

    st.markdown(texts["download_label"])

    # ---- TXT download ----
    st.download_button(
        label=texts["download_txt"],
        data=edited_result,
        file_name="test_senaryosu.txt",
        mime="text/plain",
    )

    # ---- PDF download ----
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Test Senaryosu", ln=True, align="C")

        def body(self, text: str):
            self.set_font("Arial", "", 11)
            self.multi_cell(0, 10, text)

    pdf = PDF()
    pdf.add_page()
    pdf.body(remove_accents(edited_result))
    pdf_bytes = pdf.output(dest="S").encode("latin1")

    st.download_button(
        label=texts["download_pdf"],
        data=pdf_bytes,
        file_name="test_senaryosu.pdf",
        mime="application/pdf",
    )
