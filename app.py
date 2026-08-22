import os
import streamlit as st

from rag.vectordb import build_database
from graph.workflow import run_workflow


st.set_page_config(
    page_title="Multi-Agent RAG",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent RAG Assistant")

st.write("Upload your PDF and chat with it.")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    os.makedirs("docs", exist_ok=True)

    pdf_path = os.path.join(
        "docs",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())

    # Index only once
    if (
        "indexed_pdf" not in st.session_state
        or st.session_state.indexed_pdf != uploaded_file.name
    ):

        with st.spinner("Indexing PDF..."):

            build_database(pdf_path)

        st.session_state.indexed_pdf = uploaded_file.name

    st.success("PDF Indexed Successfully!")

    question = st.text_input("Ask a Question")

    if st.button("Ask"):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Thinking..."):

                answer = run_workflow(question)

            st.success("Answer")

            st.write(answer)