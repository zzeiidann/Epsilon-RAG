"""Command-line interface for querying the knowledge base."""

import argparse

from epsilon_rag.rag import query


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask Epsilon RAG a question.")
    parser.add_argument("question", help="Question to answer from indexed documents.")
    args = parser.parse_args()

    answer, sources = query(args.question)
    print(answer)
    if sources:
        print("\nSources:")
        for source in sources:
            print(f"- {source}")


if __name__ == "__main__":
    main()

