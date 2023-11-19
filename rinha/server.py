from rinha.app import app

# Handlers
from rinha.handlers import healthcheck
from rinha.handlers import pessoas


# Handler Registration
healthcheck.define_routes(app)
pessoas.define_routes(app)
