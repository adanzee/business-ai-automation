import pdfplumber
from pathlib import Path


def extract_text_from_pdf( file_path: Path) -> list:
    chunks = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            else:

                data_dict = {
                    "chunk_text":text,
                    "page_num": i+1,
                    "metadata": {
                        "source_file": Path(file_path).name,
                        "source_path": file_path, 
                        "dept": Path(file_path).parent.name
                    }
                }
                chunks.append(data_dict)

    return chunks
