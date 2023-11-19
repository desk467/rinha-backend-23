from starlette.applications import Starlette
from rinha.lifespan import lifespan

app = Starlette(lifespan=lifespan)
