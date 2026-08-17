"""Embedding model factory."""

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from epsilon_rag.config import settings


@lru_cache(maxsize=1)
def get_embedding_function() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
    )

