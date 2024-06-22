"""Main application entry point."""

import sys
import traceback
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    TurnContext,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
from botbuilder.schema import Activity

from src.bots.query_bot import QueryBot
from src.core import adapter_configuration

ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(adapter_configuration))


async def on_error(context: TurnContext, error: Exception) -> None:
    """Catch-all for errors.

    Arguments:
        context: The context object.
        error: -- The error object.
    """
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")


async def messages(req: Request) -> Response:
    """Handle incoming HTTP requests.

    Arguments:
        req: The request object.

    Returns:
        The response object.
    """
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(auth_header, activity, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)


ADAPTER.on_turn_error = on_error
BOT: QueryBot = QueryBot()
APP: web.Application = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=adapter_configuration.PORT)
    except Exception as error:
        raise error
