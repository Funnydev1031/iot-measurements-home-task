from random import random
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

HTTP_500_RATE = 0.10
HTTP_502_RATE = 0.10


class RandomFailureMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if (
            "/docs" not in request.headers.get("referer", "") and
            "/docs" not in request.url.path
        ):
            if random() < HTTP_500_RATE:
                return Response(status_code=500)
            if random() < HTTP_502_RATE:
                return Response(status_code=502)

        return await call_next(request)