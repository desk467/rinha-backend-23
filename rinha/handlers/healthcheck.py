from starlette.requests import Request
from starlette.responses import Response
from starlette.applications import Starlette


def define_routes(app: Starlette):
    app.add_route("/", handle_healthcheck, methods=["GET"])


async def handle_healthcheck(_: Request) -> Response:
    return Response(status_code=200, content="WORKING")
