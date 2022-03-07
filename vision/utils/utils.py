from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import casbin
import jinja2
import psycopg2.extras
from elasticsearch import Elasticsearch
from postgis.psycopg import register
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import session, sessionmaker

from utils import flags

VF = flags.VisionFlags.get()


@dataclass(frozen=True)
class SessionMaker:
    engine: Engine
    SessionLocal: sessionmaker


env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
env.filters["ix"] = lambda a, b: set(a) & set(b)
env.filters["diffx"] = lambda a, b: set(a) - set(b)


@dataclass(frozen=True)
class VisionDb:
    session: session.Session
    engine: Engine

    def __call__(self, *args, **kwargs):
        return self.run_sql(*args, **kwargs)

    def run_sql(self, sql, params=None, jinja_params=None):
        def _sql(sql: str):
            if isinstance(sql, Path):
                return sql.read_text()
            sql = str(sql)
            if len(str(sql)) > 220:
                return sql
            if jinja_params:
                return env.get_template(sql).render(jinja_params)
            path = Path(sql)
            if not path.is_file():
                return sql
            text = path.read_text()
            return text

        return self.session.execute(_sql(sql), params)


def _create_postgres_sessionmaker(url=None):  # pragma: no cover
    engine = create_engine(
        url or str(flags.PostgresqlFlags.get().url),
        execution_options={
            "schema_translate_map": {"vision_sources": "vision_sources"}
        },
        echo=flags.SqlAlchemyFlags.get().echo,
        connect_args={
            "options": "-c timezone=utc",
            "cursor_factory": psycopg2.extras.NamedTupleCursor,
            **(
                {}
                if not flags.PostgresqlFlags.get().ssl_mode
                else {"sslmode": "require"}
            ),
        },
        executemany_mode="values",
    )
    if not VF.debug and not VF.testing_mode:
        with engine.connect() as c:
            c.execute("select 24")
    return SessionMaker(
        engine, sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )


_postgres_sessionmaker = None


def get_postgres_sessionmaker(init_url=None) -> SessionMaker:
    global _postgres_sessionmaker
    if not _postgres_sessionmaker:
        _postgres_sessionmaker = _create_postgres_sessionmaker(init_url)
    return _postgres_sessionmaker


@contextmanager
def postgres_session():
    try:
        session = get_postgres_sessionmaker().SessionLocal()
        register(session.bind.raw_connection())
        yield VisionDb(session, get_postgres_sessionmaker().engine)
    finally:
        session.close()


class VisionEnforcer:
    def __init__(self) -> None:
        self.enforcer = casbin.Enforcer(
            str(Path(__file__).parent / "rbac/model.conf"),
            str(Path(__file__).parent / "rbac/policy.csv"),
        )
        self.enforcer.logger.error = self.enforcer.logger.info

    def enforce(self, role, path, method):
        return self.enforcer.enforce(role, path, method)


enforcer = VisionEnforcer()


class VisionSearch:
    es: Elasticsearch

    def __init__(self) -> None:
        self.es = Elasticsearch(VF.es_endpoint, timeout=300)

    def initialize(self, index_name, mappings):
        """Create or update indices and mappings"""
        if self.es.indices.exists(index=index_name):
            self.es.indices.put_mapping(index=index_name, body=mappings)
        else:
            self.es.indices.create(
                index=index_name,
                body={
                    "mappings": mappings,
                },
            )


@contextmanager
def search_session():
    try:
        vs = VisionSearch()
        yield vs
    finally:
        vs.es.close()
