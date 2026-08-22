from pypdf import PdfReader


def load_pdf(pdf_path):
    """
    Reads a PDF file and returns all its text.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


if __name__ == "__main__":

    pdf_path = "docs/dummy.pdf"
    text = load_pdf(pdf_path)

    print(text)