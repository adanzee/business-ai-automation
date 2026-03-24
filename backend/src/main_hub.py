import json
from pathlib import Path
from src.storage import ChunkStorage
from src.parser import extract_text_from_pdf
from src.chunker import chunk_document
from src.keyword_extractor import extract_keywords
from src.retriever import retrieve_chunks
from src.llm_client import generate_response


def ingest_file(file_path: Path, dept:str):
    storage = ChunkStorage()
    if storage.document_exists(str(file_path)):
        print(f"Document {file_path} already exists in the database. Skipping ingestion.")
        storage.close()
        return
    text = extract_text_from_pdf(file_path)
    title = file_path.stem
    document_id = storage.insert_document(dept, str(file_path), title)

    chunks = chunk_document(text)
    for index, chunk in enumerate(chunks):
        keywords = extract_keywords(chunk['chunk_text'])
        storage.insert_chunk(document_id, chunk['chunk_text'], index, chunk['page_num'],chunk_embedding=None, keywords=keywords, metadata=json.dumps(chunk['metadata']))
    storage.close()

if __name__ == "__main__":
    ingest_file(Path("F:\AI-Automation\data\marketing\Classic-Case-Study-Share-a-Coke-Campaign.pdf"), "Marketing")
    # Query Loop
    storage = ChunkStorage()
    while True:
        query = input("Enter your query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        relevant_chunks = retrieve_chunks(query, storage)
        output = generate_response(query, relevant_chunks)
        print(f"AI Analyst Response: {output}\n")
    storage.close()




