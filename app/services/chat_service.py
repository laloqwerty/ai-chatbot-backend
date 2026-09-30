from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama

from app.core.config import settings
from app.services.sql_chat_history import SqlChatHistory


def debug_step(x):
    print("=== Prompt output (list of messages) ===")
    for msg in x.messages:
        print(f"  [{msg.type}] {msg.content}")
    return x

def get_session_history(session_id: str):
    return SqlChatHistory(session_id)

llm = ChatOllama(
    model=settings.ollama_model,
    base_url=settings.ollama_base_url,
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