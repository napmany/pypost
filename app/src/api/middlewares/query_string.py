from fastapi import Request
from urllib.parse import urlencode
from starlette.middleware.base import BaseHTTPMiddleware


class FlattenQueryStringLists(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Flatten comma-separated query string values
        flattened = []
        for key, value in request.query_params.multi_items():
            flattened.extend((key, entry) for entry in value.split(","))

        # Update the request's query string with the flattened version
        request.scope["query_string"] = urlencode(flattened, doseq=True).encode("utf-8")

        response = await call_next(request)
        return response
