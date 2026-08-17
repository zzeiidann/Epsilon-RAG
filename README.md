<div align="center">

# Epsilon RAG

**A private, local-first knowledge assistant for Discord and the command line.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral-000000?logo=ollama&logoColor=white)](https://ollama.com/)
[![Chroma](https://img.shields.io/badge/Chroma-Vector_DB-FF6446)](https://www.trychroma.com/)
[![Discord](https://img.shields.io/badge/Discord-Bot-5865F2?logo=discord&logoColor=white)](https://discord.com/developers/docs/intro)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E.svg)](LICENSE)

</div>

Epsilon RAG turns PDF documents into a searchable local knowledge base. It retrieves the most relevant passages with Chroma, generates grounded answers through a local Ollama model, and exposes the result through a Discord bot or a lightweight CLI.

## Highlights

- Local-first generation with Ollama; document context stays on your machine.
- Incremental PDF indexing with stable chunk identifiers.
- Semantic retrieval powered by Hugging Face embeddings and Chroma.
- Discord `!ask` command plus a standalone query CLI.
- Environment-based secrets and centralized configuration.

## Architecture

```text
PDF files → text chunks → embeddings → Chroma
                                      ↓
Discord / CLI → semantic search → Ollama → grounded answer
```

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| RAG orchestration | LangChain |
| Local LLM | Ollama + Mistral |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector database | Chroma |
| Interface | Discord.py and CLI |

## Getting started

### Prerequisites

- Python 3.11 or newer
- [Ollama](https://ollama.com/) installed and running
- A Discord bot token if you want to use the Discord interface

### Installation

```bash
git clone https://github.com/zzeiidann/Epsilon-RAG.git
cd Epsilon-RAG
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
ollama pull mistral
```

Place one or more PDF files inside `data/`. This directory is intentionally ignored by Git so private documents are not published.

### Build the knowledge base

```bash
epsilon-index
```

Use `epsilon-index --reset` to rebuild the vector store from scratch.

### Ask from the terminal

```bash
epsilon-query "What are the key points in the document?"
```

### Run the Discord bot

Set `DISCORD_TOKEN` in `.env`, enable the **Message Content Intent** in the Discord Developer Portal, then run:

```bash
epsilon-bot
```

In a channel where the bot is present:

```text
!ask What does the document say about this topic?
```

## Project structure

```text
.
├── data/                       # Local PDF documents (not tracked)
├── src/epsilon_rag/
│   ├── bot.py                  # Discord interface
│   ├── cli.py                  # Terminal interface
│   ├── config.py               # Environment and paths
│   ├── embeddings.py           # Embedding model factory
│   ├── rag.py                  # Retrieval and generation
│   └── store.py                # PDF indexing pipeline
├── .env.example
├── pyproject.toml
└── README.md
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `DISCORD_TOKEN` | — | Discord bot authentication token |
| `OLLAMA_MODEL` | `mistral` | Ollama model used for generation |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Hugging Face embedding model |
| `RAG_TOP_K` | `7` | Number of document chunks retrieved |

## Privacy

PDF files, the generated Chroma database, environment secrets, and model artifacts are excluded from version control. Before publishing a previously private repository, inspect its Git history as ignored files may still exist in earlier commits.

## License

Distributed under the [MIT License](LICENSE).
