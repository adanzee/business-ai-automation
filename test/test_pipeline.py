import pytest
from backend.src.agents.parser import extract_text_from_pdf
from pathlib import Path
from backend.src.integrations.storage import ChunkStorage
def test_parse_pdf():
    pages = extract_text_from_pdf(Path(__file__).parent.parent / "data" / "marketing" / "Classic-Case-Study-Share-a-Coke-Campaign.pdf")
    #using assert to check if the extracted text is not empty
    assert len(pages) > 0, "Failed to extract text from PDF"
    assert 'chunk_text' in pages[0], "Extracted data does not contain 'chunk_text'"
    assert 'page_num' in pages[0], "Extracted data does not contain 'page_num'"
    assert 'metadata' in pages[0], "Extracted data does not contain 'metadata'"
    assert len(pages[0]['chunk_text']) > 0, "Extracted chunk text is empty"
    print("PDF parsing test passed.")
 