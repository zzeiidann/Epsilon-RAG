"""Retrieval-augmented generation service."""

from functools import lru_cache

from langchain_chroma import Chroma
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate

from epsilon_rag.config import settings
from epsilon_rag.embeddings import get_embedding_function

PROMPT_TEMPLATE = """Use only the context below to answer the question.
If the answer is not present, say that the indexed documents do not contain it.

Context:
{context}

Question: {question}
"""


@lru_cache(maxsize=1)
def get_database() -> Chroma:
    return Chroma(
        persist_directory=str(settings.chroma_path),
        embedding_function=get_embedding_function(),
    )


@lru_cache(maxsize=128)
def query(query_text: str) -> tuple[str, list[str]]:
    clean_query = query_text.strip()
    if not clean_query:
        raise ValueError("Query cannot be empty.")

    results = get_database().similarity_search_with_score(clean_query, k=settings.top_k)
    if not results:
        return "No relevant information was found in the indexed documents.", []

    context = "\n\n---\n\n".join(document.page_content for document, _ in results)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context,
        question=clean_query,
    )
    answer = Ollama(model=settings.ollama_model).invoke(prompt)
    sources = list(
        dict.fromkeys(
            str(document.metadata.get("source", "Unknown source"))
            for document, _ in results
        )
    )
    return answer, sources[:3]

