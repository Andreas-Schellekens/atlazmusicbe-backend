from typing import Any, List, Optional
from sqlalchemy import create_engine, select, MetaData
import config

def _get_connection_url() -> Optional[str]:
    # support both names used in examples
    return getattr(config, "db_connection", None) or getattr(config, "DATABASE_URL", None)

conn_str = _get_connection_url()
if not conn_str:
    raise RuntimeError("Database connection string not found in config. Set DB_CONNECTION or DATABASE_URL in env")

# create sync engine (expects a SQLAlchemy-compatible URL, e.g. postgresql+psycopg://user:pass@host/db)
engine = create_engine(conn_str, future=True)
metadata = MetaData()

def fetch_all(table) -> List[dict]:
    """
    Execute a SELECT on the given Table and return list[dict].
    """
    with engine.connect() as conn:
        stmt = select(table)
        result = conn.execute(stmt)
        # use mappings() to get dict-like RowMapping objects
        return [dict(r) for r in result.mappings().all()]
