from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from agent_engine.config.settings import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
