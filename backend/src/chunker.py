from nltk import sent_tokenize

def chunk_document(parsed_pages: list, chunk_size: int = 8) -> list:
    chunks = []
    global_index = 0 
    for page in parsed_pages:
        sentences  = sent_tokenize(page['chunk_text'])
        for i in range(0, len(sentences), chunk_size):
            chunk_sentences = sentences[i:i + chunk_size]
            chunk_text = ' | '.join(chunk_sentences)
            chunk_data = {
                "chunk_text": chunk_text, 
                "chunk_index": global_index,
                "page_num": page['page_num'],
                "metadata": page['metadata']
            }

            chunks.append(chunk_data)
            global_index += 1
    return chunks