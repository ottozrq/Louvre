import dataclasses
import json
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, Set, Type, Union

import pydantic
import requests
from pydantic.main import BaseModel, Extra

from utils import visionflags


class Link(Path):
    pass


class AutoLink(Link):
    pass


@dataclasses.dataclass(frozen=True)
class ModelResponse:
    model: "Model"
    response: requests.Response

    @property
    def time(self) -> timedelta:
        return self.response.elapsed

    @property
    def url(self) -> str:
        return self.response.request.path_url


class VisionmodelsFlags(visionflags.Flags):
    _visionflags_key = "visionmodels"
    extra: Extra = Extra.ignore


class Model(BaseModel):
    @classmethod
    def parse_lambda_event(cls, event: Union[str, Dict]):
        return (cls.parse_raw if isinstance(event, str) else cls.parse_obj)(event)

    @classmethod
    def from_response(cls, response: requests.Response):
        return cls.parse_obj(response.json())

    @classmethod
    def wrap(cls, response: requests.Response):
        return ModelResponse(cls.from_response(response), response)

    def json_dict(self, *args, **kwargs) -> Dict[str, Any]:
        return json.loads(self.json(*args, **kwargs))

    @classmethod
    def fields(cls) -> Dict[str, pydantic.Field]:
        return cls.__fields__

    def patch_equals(self, other: "Model") -> bool:
        return not self.patched_fields(other)

    def patched_fields(self, other: "Model") -> Set[str]:
        return {
            field
            for field in set(self.fields()).intersection(other.fields())
            if getattr(self, field) not in (None, getattr(other, field, None))
        }

    def patch(self, other: "Model", klass: Type["Model"]) -> "Model":
        return klass(
            **{
                field: getattr(self, field, None) or getattr(other, field)
                for field in klass.fields()
            }
        )

    class Config:
        extra = VisionmodelsFlags.get().extra.value
