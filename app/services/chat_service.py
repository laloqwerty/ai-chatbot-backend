import os

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

from app.services.sql_chat_history import SqlChatHistory


load_dotenv()

def debug_step(x):
    print("=== Prompt output (list of messages) ===")
    for msg in x.messages:
        print(f"  [{msg.type}] {msg.content}")
    return x

def get_session_history(session_id: str):
    return SqlChatHistory(session_id)

llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "gemma4:e4b"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{message}"),
])

chain = prompt | debug_step | llm

def debug_input(x):
    print("=== Input into chain (post-history-injection) ===", x)
    return x

chat_chain = RunnableWithMessageHistory(
    debug_input | chain ,
    get_session_history,
    input_messages_key="message",
    history_messages_key="history",
)