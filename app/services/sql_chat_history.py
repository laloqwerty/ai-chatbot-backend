import json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, trim_messages
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.db.session import engine
from app.db.models import MessageRow
from app.core.config import settings



def approximate_token_counter(messages) -> int:
    total_chars = sum(len(str(m.content)) for m in messages)
    return total_chars // 4

class SqlChatHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, token_counter=approximate_token_counter, max_tokens: int = settings.max_history_tokens):
        self.session_id = session_id
        self.token_counter = token_counter
        self.max_tokens = max_tokens

    @property
    def messages(self):
        with Session(engine) as db:
            rows = db.scalars(
                select(MessageRow)
                .where(MessageRow.session_id == self.session_id)
                .order_by(MessageRow.id)
            ).all()
        all_messages = messages_from_dict([json.loads(r.payload) for r in rows])
        return trim_messages(
            all_messages,
            max_tokens=self.max_tokens, 
            token_counter=approximate_token_counter, 
            strategy="last"
        )

    def add_messages(self, messages):
        with Session(engine) as db:
            db.add_all(
                MessageRow(
                    session_id=self.session_id,
                    payload=json.dumps(message_to_dict(m)),
                )
                for m in messages
            )
            db.commit()

    def clear(self):
        with Session(engine) as db:
            db.execute(delete(MessageRow).where(MessageRow.session_id == self.session_id))
            db.commit()