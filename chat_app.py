import streamlit as st
from Answer_gen import answer_question
import os
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Insight Engine", layout="wide")
st.title("📘 Insight Engine")


# ---------- FUNCTION TO OPEN PDF IN NEW TAB AT SPECIFIC PAGE ----------
def open_pdf_in_new_tab(pdf_path, page):
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_html = f"""
        <html>
        <head>
            <title>Catalog Viewer</title>
        </head>
        <body style="margin:0">
            <embed width="100%" height="100%"
                src="data:application/pdf;base64,{base64_pdf}#page={page}"
                type="application/pdf">
            </embed>
        </body>
        </html>
    """

    b64_html = base64.b64encode(pdf_html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64_html}" target="_blank">📄 Open Catalog Page {page}</a>'
    return href
# ----------------------------------------------------------------------


query = st.text_input("Ask about products...")

if query:
    answer, docs = answer_question(query)

    st.markdown("### 💡 Answer")
    st.write(answer)

    st.markdown("### 📚 Sources")

    for idx, d in enumerate(docs):
        st.markdown("---")
        col1, col2 = st.columns([1, 3])

        # ---------- IMAGE COLUMN ----------
        with col1:
            img = d.get("image_path")
            if img and os.path.exists(img):
                st.image(img, width=120)
            else:
                st.write("No image")

        # ---------- INFO COLUMN ----------
        with col2:
            st.markdown(f"**Product:** {d.get('product_name','Unknown')}")
            st.markdown(f"**Source File:** {d.get('source_file')}")
            st.markdown(f"**Page Number:** {d.get('page_number')}")

            pdf_path = d.get("pdf_path")
            page = d.get("page_number")

            if pdf_path and page != "N/A":
                filename = os.path.basename(pdf_path)

                # Local file server URL
                pdf_url = f"http://localhost:9000/{filename}#page={page}&toolbar=1&navpanes=0"

                st.markdown(
                    f"[📄 Open Catalog Page {page}]({pdf_url})",
                    unsafe_allow_html=True
                )
            else:
                st.warning("PDF not available.")
