import contextlib
from rinha import database
from rinha.models.pessoa import setup_pessoa_listener


@contextlib.asynccontextmanager
async def lifespan(app):
    main_conn = await database.get_database_connection()
    pool = await database.get_connection_pool()
    await setup_pessoa_listener(main_conn)

    yield {
        "pool": pool,
    }

    await main_conn.close()
    await pool.close()
