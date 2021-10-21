import logging
from typing import Dict

import models as m
import sql_models as sm
from app import app
from utils.flags import VisionFlags
from utils.utils import VisionDb


logger = logging.getLogger(__name__)

schema_show_all = VisionFlags.get().debug

TAG = m.OpenAPITag


def pruned_dict(_prune_all: bool = False, **kwargs) -> Dict:
    return {} if _prune_all else {k: v for k, v in kwargs.items() if v}


__all__ = [
    "app",
    "m",
    "sm",
    "schema_show_all",
    "TAG",
    "logger",
    "VisionDb",
]
