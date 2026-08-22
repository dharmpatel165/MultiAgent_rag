from rag.loader import load_pdf
import re


def split_text(text):
    # Split whenever a new question starts
    chunks = re.split(r'(?=Question\s+\d+|Q\d+)', text, flags=re.IGNORECASE)

    # Remove empty chunks and unnecessary spaces
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    return chunks


if __name__ == "__main__":

    pdf_text = load_pdf("docs/OS_Assessment_Merged.pdf")

    chunks = split_text(pdf_text)

    print(f"\nTotal Chunks : {len(chunks)}\n")

    for i, chunk in enumerate(chunks):

        print("=" * 50)
        print(f"Chunk {i+1}")
        print("=" * 50)
        print(chunk)
        print()