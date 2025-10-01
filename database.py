from typing import List, Optional
from sqlalchemy import create_engine, select, MetaData
from sqlalchemy.engine import Engine
import config

metadata = MetaData()
_engine: Optional[Engine] = None

def _get_connection_url() -> Optional[str]:
    # config.db_connection is set from env in config.py (falls back to DATABASE_URL)
    return getattr(config, "db_connection", None) or getattr(config, "DATABASE_URL", None)

def _get_engine() -> Engine:
    global _engine
    if _engine is None:
        conn_str = _get_connection_url()
        if not conn_str:
            raise RuntimeError(
                "Database connection string not set. Set DB_CONNECTION or DATABASE_URL environment variable on the host."
            )
        try:
            # create_engine is lazy w.r.t. network; errors from invalid URL will surface here
            _engine = create_engine(conn_str, future=True)
        except Exception as exc:
            raise RuntimeError(f"Failed to create DB engine: {exc}") from exc
    return _engine

def fetch_all(table) -> List[dict]:
    """
    Execute a SELECT on the given SQLAlchemy Table and return list[dict].
    """
    engine = _get_engine()
    with engine.connect() as conn:
        stmt = select(table)
        result = conn.execute(stmt)
        return [dict(r) for r in result.mappings().all()]
