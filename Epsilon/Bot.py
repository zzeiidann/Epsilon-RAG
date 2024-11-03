import asyncio
import discord
from discord.ext import commands
import argparse
from concurrent.futures import ThreadPoolExecutor
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function
from functools import lru_cache
import time  

executor = ThreadPoolExecutor(max_workers=32)
 
# Bot setup
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

@lru_cache(maxsize=128) 
def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=7)

    # Filter out specific sources
    filtered_results = [(doc, score) for doc, score in results if doc.metadata.get("id", None) not in ['data/Singkat.pdf', 'data/Singkat (1).pdf']]

    if not filtered_results:
        return "No relevant information found in the database."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in filtered_results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in filtered_results]
    sources_to_display = sources[:3]

    formatted_response = f"Response: {response_text}\n"
    return formatted_response

async def query_rag_async(query_text: str):
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(executor, query_rag, query_text)
    return response

# Bot command to handle queries
@bot.command(name="ask")
async def ask(ctx, *, query_text: str):
    start_time = time.time()  # Mencatat waktu mulai
    response = await query_rag_async(query_text)
    elapsed_time = time.time() - start_time  # Menghitung waktu yang berlalu
    await ctx.send(f"{response}\n\nTime taken: {elapsed_time:.2f} seconds")  # Mengirimkan respons dan waktu

# Log the bot's status
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# Run the bot with your token
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("token", type=str, help="The Discord bot token.")
    args = parser.parse_args()
    bot.run(args.token)
