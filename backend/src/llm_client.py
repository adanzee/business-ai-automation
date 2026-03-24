

import requests
from pathlib import Path
import json




def build_context(chunks: list[dict]) -> str:
    context = []
    for i, chunk in enumerate(chunks):
        text = chunk['chunk_text'].replace('|', ' ')
        metadata = json.loads(chunk['metadata'])
        citation = f"[Source {i+1}: {metadata['source_file']}, Page {chunk['page_num']}]"
        formatted = f"{citation}\n{text}"
        context.append(formatted)
    return "\n\n".join(context)


def generate_response(query:str, chunks: list[dict]) -> str:

    context = build_context(chunks)
    prompt = f"""You are an AI analyst. Answer only from the context below.
    Always end your answer with the citation in this exact format:
    Source: [filename], Page: [page number]

    If the answer is not in the context say 'Insufficient data'.
    Re-quote any statistics or citations exactly as they appear.

    Context:
    {context}

    Question: {query}
    Answer:"""

    response = requests.post(
        url = "http://localhost:11434/api/generate",
        json = {
            "model" : "phi4-mini",
            "prompt" : prompt,
            "stream" : False,
            "options": {
                "temperature": 0.1,
                "num_predict": 250,
            }
        }
    )

    

    if response.status_code == 200:
        return response.json().get("response")
    else:   
        raise Exception(f"Failed to generate response: {response.status_code} - {response.text}")
    
    

    
