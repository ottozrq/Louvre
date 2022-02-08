"""Configuration setup for pytest"""
import postgis
import pytest
import sqlalchemy
import testing.postgresql
from fastapi import testclient
from passlib.context import CryptContext
from sqlalchemy.orm import scoped_session

import depends as d
import sql_models as sm
from app import get_app
from tests import fixtures as fixts
from tests import utils
from utils.utils import VisionDb

from .sqlalchemy_fixture_factory.sqla_fix_fact import SqlaFixFact

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="session")
def app():
    with testing.postgresql.Postgresql() as p:
        app = get_app(url=p.url())
        session = app.postgres_sessionmaker.SessionLocal()

        for extension in (
            "postgis",
            "uuid-ossp",
        ):
            session.execute(f'create extension if not exists "{extension}";')
        for schema in ("vision_sources",):
            session.execute(f'create schema if not exists "{schema}";')
        session.commit()
        sm.PsqlBase.metadata.create_all(session.bind)
        session.close()
        yield app


@pytest.fixture
def _api_client(app, monkeypatch, mocker):
    # Start a transaction
    connection = app.postgres_sessionmaker.engine.connect()
    transaction = connection.begin()

    session = scoped_session(
        app.postgres_sessionmaker.SessionLocal, scopefunc=lambda: ""
    )
    postgis.psycopg.register(session.bind.raw_connection())
    connection.force_close = connection.close
    transaction.force_rollback = transaction.rollback

    connection.close = lambda: None
    transaction.rollback = lambda: None
    session.close = lambda: None
    # Begin a nested transaction (any new transactions created in the codebase
    # will be held until this outer transaction is committed or closed)
    session.begin_nested()

    # Each time the SAVEPOINT for the nested transaction ends, reopen it
    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, trans):
        if trans.nested and not trans._parent.nested:
            # ensure that state is expired the way
            # session.commit() at the top level normally does
            session.expire_all()

            session.begin_nested()

    # Force the connection to use nested transactions
    connection.begin = connection.begin_nested

    # If an object gets moved to the 'detached' state by a call to flush the session,
    # add it back into the session (this allows us to see changes made to objects
    # in the context of a test, even when the change was made elsewhere in
    # the codebase)
    @sqlalchemy.event.listens_for(session, "persistent_to_detached")
    @sqlalchemy.event.listens_for(session, "deleted_to_detached")
    def rehydrate_object(session, obj):
        session.add(obj)

    try:
        fix = SqlaFixFact(session)

        def override_get_db():
            try:
                session.begin_nested()
                yield VisionDb(session, app.postgres_sessionmaker.engine)
            finally:
                session.commit()
                session.close()

        app.dependency_overrides[d.get_psql] = override_get_db
        mocks = utils.Mocks.make(mocker)
        yield utils.ApiClient(
            db=VisionDb(session, app.postgres_sessionmaker.engine),
            app=app,
            # base_url is added to get around le-village WIFI problem.
            client=testclient.TestClient(app, base_url="http://127.0.0.1"),
            fix=fix,
            session=session,
            mocks=mocks,
            user=None,
            default_user=None,
        )
    finally:
        session.remove()
        transaction.force_rollback()
        connection.force_close()
        assert not session.query(sm.Landmark).count()


@pytest.fixture
def fix(_api_client: utils.ApiClient):
    return _api_client.fix


@pytest.fixture
def cl(api_client) -> utils.ApiClient:
    return api_client


@pytest.fixture
def api_client(_api_client: utils.ApiClient, user_admin) -> utils.ApiClient:
    _api_client.user = user_admin
    _api_client.default_user = _api_client.user
    _api_client.login(user_admin, superuser=True)
    yield _api_client


@pytest.fixture
def user_admin(fix):
    return fixts.User(
        fix,
        user_email="otto@ottozhang.com",
        password=pwd_context.hash("666666"),
        user_id="00000000-0000-0000-0000-000000000001",
        role=sm.UserRole.admin,
    ).create()


@pytest.fixture
def user_editor(fix):
    return fixts.User(
        fix,
        user_email="editor@ottozhang.com",
        password=pwd_context.hash("666666"),
        user_id="00000000-0000-0000-0000-000000000002",
        role=sm.UserRole.editor,
    ).create()


@pytest.fixture
def landmark_1(fix):
    return fixts.Landmark(
        fix,
        landmark_id=1,
    ).create()


@pytest.fixture
def artwork_1(fix, landmark_1):
    return fixts.Artwork(
        fix,
        artwork_id=1,
        landmark=landmark_1,
    ).create()


@pytest.fixture
def series_1(fix, landmark_1, user_editor):
    return fixts.Series(
        fix,
        landmark=landmark_1,
        author=user_editor,
    ).create()


@pytest.fixture
def introduction_1(fix, artwork_1, series_1):
    return fixts.Introduction(
        fix,
        artwork=artwork_1,
        series=series_1,
    ).create()
