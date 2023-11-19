import contextlib
from rinha import database
from rinha.models.pessoa import Pessoa


@contextlib.asynccontextmanager
async def lifespan(app):
    pool = await database.get_connection_pool()

    # Database creation
    await Pessoa.generate_table(pool)

    yield {
        "pool": pool,
    }

    await pool.close()
