from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    future=True,
    max_overflow=10,
    pool_size=20,
    pool_timeout=30,
    pool_recycle=1800,
)



if engine.url.get_backend_name() == "sqlite":
    @event.listens_for(engine.sync_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record) -> None:
        """Aplica PRAGMAs do SQLite ao conectar.

        Ativa o modo WAL, define a sincronização como NORMAL e habilita
        chaves estrangeiras.

        Args:
            dbapi_connection: Objeto de conexão DB-API fornecido pelo
                SQLAlchemy.
            connection_record: Registro da conexão (não utilizado).
        """

        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
