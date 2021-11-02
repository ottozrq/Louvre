import logging
from typing import Dict

from fastapi import HTTPException, Response, status

import depends as d
import models as m
import sql_models as sm
from app import app
from utils import algo
from utils.flags import VisionFlags
from utils.utils import VisionDb


delete_response = Response(status_code=status.HTTP_204_NO_CONTENT)

logger = logging.getLogger(__name__)

schema_show_all = VisionFlags.get().debug

TAG = m.OpenAPITag


def pruned_dict(_prune_all: bool = False, **kwargs) -> Dict:
    return {} if _prune_all else {k: v for k, v in kwargs.items() if v}


__all__ = [
    "algo",
    "app",
    "d",
    "m",
    "sm",
    "schema_show_all",
    "TAG",
    "logger",
    "VisionDb",
    "HTTPException",
]
