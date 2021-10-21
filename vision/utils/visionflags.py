import json
import logging
from pathlib import Path
from typing import Any, Dict, Set, Type, TypeVar

import pydantic
import yaml
from pydantic import BaseSettings, root_validator
from pydantic.fields import Field

from utils import config

logger = logging.getLogger(__name__)

_SECRETS_DIR = ".secrets"


def Secret(secret: str) -> pydantic.Field:
    return Field(
        default_factory=lambda: config.secrets.get(secret),
        description=f"AWS Secret '`{secret}`'",
    )


class _Meta(type(pydantic.BaseSettings)):
    def __new__(cls, name, bases, dct):
        if key := dct.get("_visionflags_key"):
            dct.setdefault("Config", type("Config", (), {})).env_prefix = f"{key}_"
        return super().__new__(cls, name, bases, dct)


class _Visionflags(BaseSettings, metaclass=_Meta):
    _visionflags_key = "visionflags"
    file: Path = None
    contents: str = None
    contents_json: str = None
    target: str = None
    use_env_settings: bool = True
    verbose: bool = False

    @root_validator
    def more_than_1_set(cls, values: Dict[str, Any]):
        check_values = {k: values[k] for k in {"file", "contents", "contents_json"}}
        if len([x for x in check_values.values() if x]) > 1:
            raise Exception(f"Only 1 configuration may be specified: {check_values}")
        return values

    @classmethod
    def secrets_dir(cls) -> Path:
        base = Path(_SECRETS_DIR)
        extended = base / (cls().target or "")
        return extended if extended.is_dir() else base

    @property
    def spec(self) -> Dict[str, Any]:
        root = {}
        if self.contents:
            root = yaml.safe_load(self.contents)
        elif self.contents_json:
            root = json.loads(self.contents_json)
        elif self.file and (path := Path(self.file)).is_file():
            root = yaml.safe_load(path.read_text())

        targets = root.pop("targets", {})

        def merge(a, b):
            return {
                **a,
                **{
                    k: {**a.get(k, {}), **v} if isinstance(v, dict) else v
                    for k, v in b.items()
                },
            }

        def get_target(t):
            if not t:
                return {}
            target = targets.get(t, {})
            return merge(get_target(target.pop("extends", None)), target)

        return merge(root, get_target(self.target))


class Flags(BaseSettings, metaclass=_Meta):
    """visionflags settings. See `/visionflags.md`."""

    _T = TypeVar("_T", bound="Flags")
    _default: _T = None
    _visionflags_key: str = None
    _registry: Set[_T] = set()

    def _visionflags_log(self):
        if logging.root.level > logging.INFO:
            logging.basicConfig(level=logging.INFO)
        logger.info(
            f"""

        {self.__class__.__name__}

{self.json(indent=2)}

"""
        )

    @classmethod
    def __init_subclass__(cls):
        if cls._visionflags_key:
            for c in cls._registry:
                if c._visionflags_key == cls._visionflags_key:
                    raise Exception(
                        f"Cannot register visionflags {cls}."
                        + f"_visionflags_key {cls._visionflags_key}"
                        + f" already registered by {c}"
                    )
        cls._registry.add(cls)

    @classmethod
    def full_schema(cls) -> str:
        def _fix(x):
            x.__doc__ = f"""{x.__doc__ or Flags.__doc__ or ''}

`visionflags_key` = *`{x._visionflags_key}`*
"""
            return x

        return pydantic.create_model(
            "Visionflags",
            **{x.__name__: (_fix(x), ...) for x in cls._registry},
        ).schema_json()

    class Config:
        validate_all = False

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            base = (
                cls._from_yaml,
                file_secret_settings,
                init_settings,
            )
            if _Visionflags().use_env_settings:
                return (env_settings, *base)
            return base

        @classmethod
        def _from_yaml(cls, instance) -> Dict[str, Any]:
            spec = _Visionflags().spec
            return (
                spec.get(instance._visionflags_key, {})
                if instance._visionflags_key
                else spec
            )

    @classmethod
    def get(cls: Type[_T]) -> _T:
        if cls is Flags:
            raise Exception("cannot get base Flags class, please subclass")
        if cls._default:
            return cls._default
        cls._default = cls._default or cls(_secrets_dir=_Visionflags().secrets_dir())
        if _Visionflags().verbose:
            cls._default._visionflags_log()
        return cls._default
