import sys
from pathlib import Path
#PROJECT_ROOT = Path(__file__).parent
#sys.path.insert(0, str(PROJECT_ROOT / "src"))

import argparse
from src.storage import ChunkStorage
from rich.console import Console



console = Console()

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
        