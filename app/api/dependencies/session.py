"""Dependências de sessão do banco de dados.

Este módulo fornece a configuração e gerenciamento de sessões assíncronas
do SQLAlchemy para a aplicação.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.database import engine

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Fornece uma sessão assíncrona do banco de dados.

    Gerencia o ciclo de vida da sessão, incluindo rollback automático em caso
    de exceção e fechamento apropriado da conexão.

    Yields:
        AsyncSession: Uma sessão assíncrona do SQLAlchemy.

    Raises:
        Exception: Qualquer exceção ocorrida durante a operação é propagada
            após o rollback automático.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
