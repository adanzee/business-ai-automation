from src.storage import ChunkStorage
from src.keyword_extractor import extract_keywords

def retrieve_chunks(query:str, storage: ChunkStorage, top_chunk: int = 5) -> list:
    # Extract keywords from the user query
    user_keywords = extract_keywords(query).split(',')
    
    # Retrieve all chunks from the database
    all_chunks = storage.get_all_chunks()
    # Filter chunks based on keyword matching
    keywords = []
    for chunk in all_chunks:
        chunk_keywords = chunk['keywords'].split(',')
        match_keywords = set (user_keywords) & set(chunk_keywords)
        if match_keywords:
            chunk_dict = dict(chunk)
            count = len(match_keywords)
            chunk_dict['match_count'] = count
            keywords.append(chunk_dict)
    # Sort chunks based on the descending order of matching keywords
    sorted_chunks = sorted(keywords, key=lambda x: x['match_count'], reverse=True)
    # Return the top N chunks    
    return  sorted_chunks[:top_chunk]
 
        