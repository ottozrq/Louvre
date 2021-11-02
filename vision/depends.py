import logging
from typing import Optional

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import PositiveInt
from pydantic.types import constr

import models as m
from utils import flags
from utils.utils import VisionDb, postgres_session


class _Bearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        return not flags.VianovaFlags.get().superuser_email and await super(
            _Bearer, self
        ).__call__(request)


security = _Bearer("/token/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_psql() -> VisionDb:
    with postgres_session() as psql:
        yield psql


def get_pagination(
    request: Request,
    page_token: constr(regex=r"\d+") = None,  # noqa
    page_size: PositiveInt = None,
):
    return m.Pagination(request=request, page_size=page_size, page_token=page_token)
