import pathlib
import re
from typing import Any, Dict, List

from pydantic.class_validators import root_validator
from pydantic.networks import HttpUrl

from utils.visionflags import Flags, Secret


class PostgresqlFlags(Flags):
    _visionflags_key = "vision_pg"

    host: str

    password: str = Secret("aurora_cluster_master_password")

    database: str = "vision"
    schema_prefix: str = "vision_sources"
    username: str = "vision"

    ssl_mode: bool = True

    @property
    def url(self):
        from sqlalchemy.engine.url import URL

        return URL(
            drivername="postgresql",
            username=self.username,
            host=self.host,
            database=self.database,
            port=5432,
            password=self.password,
        )


class SqlAlchemyFlags(Flags):
    _visionflags_key = "sqlalchemy"

    echo: bool = False
    track_modifications: bool = False
    alembic_env: str = None


class VisionFlags(Flags):
    _visionflags_key = "vision"

    class Config:
        fields = {"namespace": {"env": "namespace"}}

    namespace: str
    login_secret: str
    superuser_email: str = None

    # cognito_cert_1: str = Secret("jwt_public_key_cognito_1")
    # cognito_cert_2: str = Secret("jwt_public_key_cognito_2")
    # salt: str = Secret("salt")

    eb_endpoint: str = "http://localhost:4572"
    lambda_endpoint: str = "https://lambda.eu-central-1.amazonaws.com"
    sm_endpoint: str = "https://secretsmanager.eu-central-1.amazonaws.com"
    cors_urls: List[HttpUrl] = []

    display_traceback: bool = False
    debug: bool = False
    testing_mode: bool = False

    root_path: pathlib.Path = None

    allow_origin_regex: re.Pattern = re.compile(
        r"^(http://(.*\.)?localhost:\d+|https://.*\.vision\.(dev|io))/?$"
    )

    @root_validator
    def compatible_testing_mode(cls, values: Dict[str, Any]):
        testing_mode = values.get("testing_mode")
        namespace = values.get("namespace")
        if testing_mode and any(k in namespace for k in ("staging", "production")):
            raise ValueError(
                "`testing_mode` cannot be true when "
                + "('staging', 'production') in `NAMESPACE`"
            )
        return values


class BulkSettings(Flags):
    _visionflags_key = "bulk_settings"
    fast_save = False

    @classmethod
    def use_fast_save(cls, creations: List):
        return cls.get().fast_save or len(creations) >= 1000
