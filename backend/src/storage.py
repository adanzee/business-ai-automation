import sqlite3
from pathlib import Path
from .config import settings


class ChunkStorage:
    def __init__(self):
        self.db_path = Path(settings.DB_PATH).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init_tables()

    def _init_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS documents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept TEXT NOT NULL,
            file_path TEXT NOT NULL,
            title TEXT, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )

            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            chunk_index INTEGER,
            page_num INTEGER,  --for PDF citation
            chunk_embedding BLOB,
            keywords TEXT, --for retrieval augmentation, JSON string of list of keywords
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(document_id) REFERENCES documents(id)
            )

            """
        )

        self.conn.commit()
        print(f"Initialized database at {self.db_path}")


    def insert_document(self, dept:str, file_path: str, title:str):
        self.cursor.execute(
            """
            INSERT INTO documents (dept, file_path, title) VALUES (?, ?, ?)
            """,
            (dept, file_path, title)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    

    def insert_chunk(self, document_id:int, chunk_text:str, chunk_index:int, page_num:int, chunk_embedding:bytes, keywords:str, metadata:str):
        self.cursor.execute(
            """
            INSERT INTO chunks(document_id, chunk_text, chunk_index, page_num, chunk_embedding, keywords, metadata) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (document_id, chunk_text, chunk_index, page_num, chunk_embedding, keywords, metadata)
        )

        self.conn.commit()
        return self.cursor.lastrowid
    

    def document_exists(self, file_path:str) -> bool:
        self.cursor.execute(
            """
            
            SELECT id FROM documents WHERE file_path = ? 
            """,
            (file_path,)
        )
        return self.cursor.fetchone() is not None 

    def close(self):
        self.conn.close()

