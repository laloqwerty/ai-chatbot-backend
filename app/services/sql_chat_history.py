import json
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.db.session import engine
from app.db.models import MessageRow


class SqlChatHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.session_id = session_id

    @property
    def messages(self):
        with Session(engine) as db:
            rows = db.scalars(
                select(MessageRow)
                .where(MessageRow.session_id == self.session_id)
                .order_by(MessageRow.id)
            ).all()
        return messages_from_dict([json.loads(r.payload) for r in rows])

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