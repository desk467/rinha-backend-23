import asyncpg


async def get_connection_pool():
    return await asyncpg.create_pool(
        "postgresql://rinha:segredo@postgres:5432/rinha", max_size=10
    )
