from starlette.requests import Request
from starlette.background import BackgroundTask
from starlette.responses import Response, JSONResponse
from starlette.datastructures import Headers
from starlette.applications import Starlette
from rinha.models.pessoa import Pessoa
from rinha.tasks import pessoa_buffer


def define_routes(app: Starlette):
    app.add_route("/pessoas/{pessoa_id}", get_pessoa, methods=["GET"])
    app.add_route("/pessoas", get_pessoa_by_term, methods=["GET"])
    app.add_route("/pessoas", create_pessoa, methods=["POST"])
    app.add_route("/contagem-pessoas", contagem_pessoa, methods=["GET"])


async def create_pessoa(request: Request) -> Response:
    req_data = await request.json()
    new_pessoa = Pessoa.build(req_data)
    pessoa_buffer.add_item(new_pessoa)

    task = BackgroundTask(pessoa_buffer.bulk_insert_task, pool=request.state.pool)

    return Response(
        headers=Headers({"Location": f"/pessoas/{new_pessoa.id}"}),
        status_code=201,
        background=task,
    )


async def get_pessoa_by_term(request: Request) -> Response:
    termo = request.query_params.get("t")

    pessoas = await Pessoa.get_from_term(request.state.pool, termo)
    return JSONResponse([pessoa.as_dict() for pessoa in pessoas])


async def get_pessoa(request: Request) -> Response:
    pessoa_id = request.path_params.get("pessoa_id")

    pessoa = await Pessoa.get(request.state.pool, pessoa_id)
    return JSONResponse(pessoa.as_dict())


async def contagem_pessoa(request: Request) -> Response:
    count = await Pessoa.count(request.state.pool)

    return Response(content=f"count={count}", status_code=200)
