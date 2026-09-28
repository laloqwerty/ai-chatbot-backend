#engine + Session factory (reads DATABASE_URL)

import os
from sqlalchemy import create_engine
from app.db.models import Base

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///chat.db"))
Base.metadata.create_all(engine)  # fine for now; swap for Alembic later