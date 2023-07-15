from sqlalchemy import create_engine, text, Column, Integer, String, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


_BASE = declarative_base()


class Task(_BASE):
    __tablename__ = 'tasks'
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(50), nullable=False)
    done = Column("done", Boolean, nullable=False)

    def __init__(self, name:str, done:bool=False):
        self.name = name
        self.done = done
    
    def __repr__(self):
        return f'<Task name:{self.name!r}, done:{self.done}>'


_SQL_ENGINE = create_engine('sqlite:///tasks.db', echo=True)
_DB_SESSION = scoped_session(sessionmaker(
        autoflush=False,
        bind=_SQL_ENGINE
    ))
_BASE.query = _DB_SESSION.query_property()


def init() -> None:
    """
    Initialize the SQL engine and the app's database.
    This must be called before using any other methods in this module.
    """
    global _SQL_ENGINE, _DB_SESSION, _BASE
    _BASE.metadata.create_all(bind=_SQL_ENGINE)
