

import requests
from pathlib import Path
import json
from src.config import settings



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
    prompt = f"""You are an AI analyst for a company. 
    Include source citation at the end.
    Reproduce statistics and quotes exactly as they appear.
    Only say 'Insufficient data' if context has NO relevant information at all.
    Never mix an answer with 'Insufficient data' — choose one or the other.

    Context:
    {context}

    Question: {query}

    Answer (must be based on context above, include citation):"""

    response = requests.post(
        url = "http://localhost:11434/api/generate",
        json = {
            "model" : settings.MODEL_NAME,
            "prompt" : prompt,
            "stream" : False,
            "options": {
                "temperature": 0.1,
                "num_predict": 400,
            }
        }
    )

    

    if response.status_code == 200:
        return response.json().get("response")
    else:   
        raise Exception(f"Failed to generate response: {response.status_code} - {response.text}")
    
    

    
