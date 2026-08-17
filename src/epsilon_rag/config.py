"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    data_path: Path = PROJECT_ROOT / "data"
    chroma_path: Path = PROJECT_ROOT / "chroma"
    ollama_model: str = os.getenv("OLLAMA_MODEL", "mistral")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    top_k: int = int(os.getenv("RAG_TOP_K", "7"))


settings = Settings()

