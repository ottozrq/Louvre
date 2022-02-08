import logging
from typing import Optional

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import PositiveInt
from pydantic.types import constr

import models as m
import sql_models as sm
from utils import flags
from utils.utils import VisionDb, postgres_session


class _Bearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        return not flags.VisionFlags.get().superuser_email and await super(
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


def get_user_id(
    request: Request,
    _=Depends(security),
) -> str:
    return str(request.user.user_uuid)


def get_user_email(
    request: Request,
    _=Depends(security),
) -> str:
    return str(request.user.user_email)


def get_logged_in_user(
    user_id=Depends(get_user_id),
    db=Depends(get_psql),
) -> sm.User:
    return m.User.db(db).get_or_404(user_id)


def superuser_email() -> str:
    return flags.VisionFlags.get().superuser_email


def user_owned_series(
    series_id: int,
    user: sm.User = Depends(get_logged_in_user),
    db: VisionDb = Depends(get_psql),
) -> sm.Series:
    if user.own_series(series_id):
        return m.Series.db(db).get_or_404(series_id)
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot access series")


def user_owned_introductions(
    introduction_id: int,
    user: sm.User = Depends(get_logged_in_user),
    db: VisionDb = Depends(get_psql),
) -> sm.Series:
    if user.own_series(introduction_id):
        return m.Introduction.db(db).get_or_404(introduction_id)
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Cannot access series")
