"""Build and maintain the local Chroma document index."""

import argparse
import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from epsilon_rag.config import settings
from epsilon_rag.embeddings import get_embedding_function


def load_documents(data_path: Path = settings.data_path) -> list[Document]:
    data_path.mkdir(parents=True, exist_ok=True)
    return PyPDFDirectoryLoader(str(data_path)).load()


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=70,
        length_function=len,
        is_separator_regex=False,
    )
    return assign_chunk_ids(splitter.split_documents(documents))


def assign_chunk_ids(chunks: list[Document]) -> list[Document]:
    """Assign stable IDs based on source, page, and position on the page."""
    last_page_id: str | None = None
    chunk_index = 0

    for chunk in chunks:
        page_id = f"{chunk.metadata.get('source')}:{chunk.metadata.get('page')}"
        chunk_index = chunk_index + 1 if page_id == last_page_id else 0
        chunk.metadata["id"] = f"{page_id}:{chunk_index}"
        last_page_id = page_id

    return chunks


def update_index(chunks: list[Document]) -> int:
    database = Chroma(
        persist_directory=str(settings.chroma_path),
        embedding_function=get_embedding_function(),
    )
    existing_ids = set(database.get(include=[])["ids"])
    new_chunks = [chunk for chunk in chunks if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        database.add_documents(
            new_chunks,
            ids=[chunk.metadata["id"] for chunk in new_chunks],
        )
    return len(new_chunks)


def reset_index() -> None:
    if settings.chroma_path.exists():
        shutil.rmtree(settings.chroma_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Index PDF documents for Epsilon RAG.")
    parser.add_argument("--reset", action="store_true", help="Rebuild the index from scratch.")
    args = parser.parse_args()

    if args.reset:
        reset_index()

    documents = load_documents()
    if not documents:
        raise SystemExit(f"No PDF files found in {settings.data_path}")

    added = update_index(split_documents(documents))
    print(f"Indexed {added} new chunks from {len(documents)} document pages.")


if __name__ == "__main__":
    main()

