import asyncpg


def get_database_url():
    return "postgresql://rinha:segredo@postgres:5432/rinha"


async def get_database_connection():
    return await asyncpg.connect(get_database_url())


async def get_connection_pool():
    return await asyncpg.create_pool(get_database_url(), max_size=10)
