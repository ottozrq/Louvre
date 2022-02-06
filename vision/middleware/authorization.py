import starlette_context
from casbin.enforcer import Enforcer
from starlette import status
from starlette.authentication import BaseUser
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from utils import flags


class CasbinMiddleware:
    """
    Middleware for Casbin
    from https://github.com/pycasbin/fastapi-authz
    """

    def __init__(
        self,
        app: ASGIApp,
        enforcer: Enforcer,
    ) -> None:
        """
        Configure Casbin Middleware
        :param app:Retain for ASGI.
        :param enforcer:Casbin Enforcer, must be initialized before FastAPI start.
        """
        self.app = app
        self.enforcer = enforcer

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            if scope["type"] not in ("http", "websocket") or await self._enforce(
                scope, receive
            ):
                await self.app(scope, receive, send)
                return
            if Request(scope, receive).user.is_authenticated:
                raise HTTPException(status.HTTP_403_FORBIDDEN, "Unauthorized")
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
        except HTTPException as e:
            await JSONResponse(
                status_code=e.status_code,
                content=dict(detail=e.detail),
            )(scope, receive, send)

    async def _enforce(self, scope: Scope, receive: Receive) -> bool:
        """
        Enforce a request
        :param user: user will be sent to enforcer
        :param request: ASGI Request
        :return: Enforce Result
        """
        request = Request(scope, receive)
        path = request.url.path
        root_path = flags.VisionFlags.get().root_path
        if root_path:
            root_path = str(root_path)
            if path.startswith(root_path):
                prefix_length = len(root_path)
                path = path[prefix_length:]
        method = request.method
        if "user" not in scope:
            raise RuntimeError(
                "Casbin Middleware must work with an Authentication Middleware"
            )
        if not request.user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
        assert isinstance(request.user, BaseUser)
        role = (
            request.user.role_string if request.user.is_authenticated else "anonymous"
        )
        starlette_context._enforcer = self.enforcer
        starlette_context.context["_enforcer_cache"] = {}
        starlette_context.context["user_role"] = role
        return self.enforcer.enforce(role, path, method)
