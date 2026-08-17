"""Discord interface for Epsilon RAG."""

import asyncio
import os
from time import perf_counter

import discord
from discord.ext import commands

from epsilon_rag.rag import query


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.command(name="ask")
    async def ask(ctx: commands.Context, *, question: str) -> None:
        started_at = perf_counter()
        try:
            answer, sources = await asyncio.to_thread(query, question)
        except Exception as error:
            await ctx.send(f"Unable to answer the question: {error}")
            return

        source_text = "\n".join(f"- {source}" for source in sources)
        response = answer
        if source_text:
            response += f"\n\nSources:\n{source_text}"
        response += f"\n\nCompleted in {perf_counter() - started_at:.2f}s"
        await ctx.send(response[:2000])

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user}")

    return bot


def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN is missing. Copy .env.example to .env and set it.")
    create_bot().run(token)


if __name__ == "__main__":
    main()

