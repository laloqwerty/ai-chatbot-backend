#engine + Session factory (reads DATABASE_URL)

from sqlalchemy import create_engine
from app.core.config import settings
from app.db.models import Base

engine = create_engine(settings.database_url)
Base.metadata.create_all(engine)  # fine for now; swap for Alembic later