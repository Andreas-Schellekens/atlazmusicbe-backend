from typing import List, Optional, Any
from sqlalchemy import create_engine, select, MetaData, text
from sqlalchemy.engine import Engine, Result
import config

metadata = MetaData()
_engine: Optional[Engine] = None

def _get_connection_url() -> Optional[str]:
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
            _engine = create_engine(conn_str, future=True)
        except Exception as exc:
            raise RuntimeError(f"Failed to create DB engine: {exc}") from exc
    return _engine

def fetch_all(table) -> List[dict]:
    engine = _get_engine()
    with engine.connect() as conn:
        stmt = select(table)
        result = conn.execute(stmt)
        return [dict(r) for r in result.mappings().all()]

def fetch_one_by_id(table, id_value: Any) -> Optional[dict]:
    engine = _get_engine()
    with engine.connect() as conn:
        stmt = select(table).where(table.c.id == id_value)
        result = conn.execute(stmt)
        row = result.mappings().first()
        return dict(row) if row is not None else None

def execute_returning(stmt) -> List[dict]:
    """
    Execute a statement inside a transaction and return list of returned rows as dicts.
    Works with INSERT ... RETURNING / UPDATE ... RETURNING.
    """
    engine = _get_engine()
    with engine.begin() as conn:
        result: Result = conn.execute(stmt)
        try:
            return [dict(r) for r in result.mappings().all()]
        except Exception:
            return []
