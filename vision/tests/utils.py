import json
import uuid
from dataclasses import dataclass
from typing import Union
from unittest.mock import MagicMock

import fastapi
import pytest_mock
import sqlalchemy.orm.session
from starlette import testclient

import depends as d
import models as m
import sql_models as sm
from middleware import authentication

from .sqlalchemy_fixture_factory.sqla_fix_fact import BaseFix, SqlaFixFact


@dataclass
class Mocks:
    # mocks are overridden in conftest.py
    auth_backend: MagicMock
    mocker: pytest_mock.MockerFixture

    @classmethod
    def make(cls, mocker):
        return cls(
            mocker=mocker,
            **{
                **{
                    k: MagicMock()
                    for k, v in cls.__dataclass_fields__.items()
                    if v.type is MagicMock
                },
                "auth_backend": mocker.patch(
                    "middleware.authentication.VisionAuthBackend.vision_user"
                ),
            },
        )


@dataclass
class ApiClient:
    db: m.VisionDb
    client: testclient.TestClient
    fix: SqlaFixFact
    session: sqlalchemy.orm.session.Session
    app: fastapi.FastAPI
    mocks: Mocks
    user: sm.User
    default_user: sm.User

    def create(self, fixture: BaseFix, *args, **kwargs):
        return fixture(self.fix, *args, **kwargs).create()

    def logout(self):
        self.app.dependency_overrides[d.superuser_email] = lambda: False
        self.app.dependency_overrides.pop(d.get_user_id)
        self.user = None
        return self

    def login(
        self,
        user: Union[m.User, sm.User, uuid.UUID, str] = None,
        superuser: bool = None,
    ):
        user = user or self.default_user
        user_id = uuid.UUID(str(getattr(user, "user_id", user)))
        user = (
            m.User.from_db(user)
            if isinstance(user, sm.User)
            else m.User.db(self.db).from_id(user_id)
        )
        self.user = m.User.db(self.db).get_or_404(user_id)
        superuser_email = superuser and user.user_email
        self.app.dependency_overrides[d.superuser_email] = lambda: superuser_email
        self.app.dependency_overrides[d.get_user_id] = lambda: user_id
        return self

    def __call__(
        self,
        url,
        method="GET",
        data=None,
        headers=None,
        status=True,
        detail=None,
        as_dict=False,
        **kwargs,
    ):
        self.session.refresh(self.user or self.default_user)
        self.mocks.auth_backend.return_value = (
            authentication.VisionAuthUser.from_user(m.User.from_db(self.user))
            if self.user
            else None
        )
        response = self.client.request(
            url=str(getattr(url, "self_link", url)),
            allow_redirects=True,
            method=method,
            headers=headers or {},
            data=dict(data)
            if as_dict
            else data
            if isinstance(data, str)
            else data.json(exclude_unset=True, exclude_none=False)
            if isinstance(data, m.Model)
            else json.dumps(data),
            **kwargs,
        )
        if status:
            assert response.status_code in {
                200 if status is True else status,
                204 if method.upper() == "DELETE" else None,
            }, "Response body is : " + response.content.decode("utf-8")
            if detail:
                actual_detail = response.json()["detail"]
                assert detail in str(actual_detail)
        return response
