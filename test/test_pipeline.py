import pytest
from backend.src.parser import extract_text_from_pdf
from backend.src.storage import ChunkStorage
def test_parse_pdf():
    test_file_path = extract_text_from_pdf(r"F:\AI-Automation\data\marketing\Classic-Case-Study-Share-a-Coke-Campaign.pdf")
    #using assert to check if the extracted text is not empty
    assert len(test_file_path) > 0, "Failed to extract text from PDF"
    assert 'chunk_text' in test_file_path[0], "Extracted data does not contain 'chunk_text'"
    assert 'page_num' in test_file_path[0], "Extracted data does not contain 'page_num'"
    assert 'metadata' in test_file_path[0], "Extracted data does not contain 'metadata'"
    assert len(test_file_path[0]['chunk_text']) > 0, "Extracted chunk text is empty"
    print("PDF parsing test passed.")
 