import sys
from pathlib import Path
#PROJECT_ROOT = Path(__file__).parent
#sys.path.insert(0, str(PROJECT_ROOT / "src"))

import argparse
from rich.console import Console
from sqlalchemy import exists

from backend.src import storage
from src.storage import ChunkStorage
from src.parser import extract_text_from_pdf
from src.chunker import chunk_document
from src.keyword_extractor import extract_keywords



console = Console()

def ingest_files(file_path: Path, dept:str, ):
   
   storage = ChunkStorage()
   
   if storage.document_exists(str(file_path)):
    return (f"{file_path} already ingested. Skipping ingestion.")
    storage.close()
   else:

    document_id = storage.insert_document(dept, str(file_path), file_path.name)
    print(f"Ingested {file_path} for department {dept}")
    parsed_pages = extract_text_from_pdf(file_path)
    chunk = chunk_document(parsed_pages)

    for chunks in chunk:
        keywords = extract_keywords(chunks['chunk_text'])
        storage.insert_chunk(
            document_id= document_id,
            chunk_text=chunks['chunk_text'],
            chunk_index=chunks['chunk_index'],
            page_num=chunks['page_num'],
            chunk_embedding=None,  # Placeholder for embedding, to be generated later
            keywords=keywords,
            metadata=str(chunks['metadata'])
        )



    storage.close() 


def main():
    parser = argparse.ArgumentParser(description="[bold:pink]Main Hub for Backend Services[bold:pink]")
    sub = parser.add_subparsers(dest="cmd", required=True, help="Available commands")
    

    ing = sub.add_parser("ingest", help="Ingest files from department folder ")
    ing.add_argument("--dept", help="Department name to ingest files from")
    ing.add_argument("--source", help="Source folder path to ingest files from")
    ing.add_argument("--dest", help="Destination folder path to store ingested files")


    args = parser.parse_args()
    print(f"Parsed command-line arguments: {args}")

    storage = ChunkStorage()

    if args.cmd == "ingest":
        console.print(f"[bold magenta]Ingesting files from [cyan]{args.source}[/cyan] for department [yellow]{args.dept}[/yellow] and storing in [magenta]{args.dest}[/magenta][/bold magenta]")
        folder = Path(args.source)
        if not folder.exists() or not folder.is_dir():
            console.print(f"[red]Error: Source folder [cyan]{args.source}[/cyan] does not exist or is not a directory.[/red]")
            return
        
        for file in folder.glob("*.*"):
         console.print(f" -> Found: {file.name}")
         console.print(f"[green]Ingesting file: [cyan]{file.name}[/cyan][/green]")

        storage.close()
if __name__ == "__main__":
    main()
        