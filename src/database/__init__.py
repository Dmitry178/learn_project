from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings

engine = create_async_engine(settings.db_url)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
