import json
import asyncio
import asyncpg
from rinha.models.pessoa import Pessoa
from rinha.util import dump_terms

inserts = set()


def add_item(p: Pessoa):
    inserts.add(p)


def generate_insertion_tuples():
    copied_inserts = list(inserts)

    for pessoa in copied_inserts:
        yield (
            pessoa.id,
            pessoa.nome,
            pessoa.apelido,
            pessoa.nascimento,
            json.dumps(pessoa.stack),
            dump_terms(pessoa.nome, pessoa.apelido, pessoa.stack),
        )
        inserts.discard(pessoa)


async def bulk_insert_task(pool: asyncpg.Pool):
    await asyncio.sleep(0.2)
    if len(inserts) == 0:
        return

    async with pool.acquire() as conn:
        await conn.executemany(
            """
            INSERT INTO t_pessoa (id, nome, apelido, nascimento, stack, termos)
            VALUES
                ($1, $2, $3, $4, $5, $6)
        """,
            list(generate_insertion_tuples()),
        )
