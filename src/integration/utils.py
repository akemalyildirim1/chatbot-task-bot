"""Utility functions for integration module."""

from typing import Any

from aiohttp import ClientSession
from pydantic import BaseModel

from src.core import RequestFailedError


class HttpResponse(BaseModel):
    """Model for HTTP response.

    Attributes:
        data: The response data.
        status: The response status.
        ok: The response status.
    """

    data: Any
    status: int
    ok: bool


async def send_http_request(
    url: str,
    method: str = "get",
    headers: dict[str, str] | None = None,
    body: Any | None = None,
) -> HttpResponse:
    """Send request to the specified url.

    Arguments:
        url: URL to send request.
        method: Method of the request.
        headers: Headers of the request.
        body: Body of the request.

    Returns:
        The dictionary that includes the response and the status.

    Raises:
        RequestFailedError: If the request fails.
    """
    raw_request_func_params: dict[str, str] = {
        "method": method,
        "url": url,
    }

    request_func_params: dict[str, str] = (
        {**raw_request_func_params, "json": body} if body else raw_request_func_params
    )

    async with ClientSession(
        headers=headers if headers else None
    ) as session, session.request(**request_func_params) as response:
        response_json: dict[str, Any] = await response.json()
        if not response.ok:
            raise RequestFailedError(
                status=response.status,
                message=response_json.get("detail"),
            )
        return HttpResponse(
            data=response_json,
            status=response.status,
            ok=response.ok,
        )
