import uuid
import json
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from typing import List, Self
from asyncpg import Pool, Connection
from rinha.util import is_valid_date, is_valid_stack


cache_pessoas = OrderedDict()
MAX_ITEMS = 800


async def setup_pessoa_listener(conn: Connection):
    await conn.add_listener("t_pessoa__insertion", insert_pessoa_callback)


async def insert_pessoa_callback(conn, pid, channel, payload):
    record = json.loads(payload)
    if not record:
        return

    cache_pessoas[record["id"]] = record

    if len(cache_pessoas) > MAX_ITEMS:
        cache_pessoas.popitem()


def get_pessoa_from_cache(pessoa_id: str):
    if pessoa := cache_pessoas.get(pessoa_id):
        return Pessoa(
            id=pessoa["id"],
            apelido=pessoa["apelido"],
            nome=pessoa["nome"],
            nascimento=datetime.strptime(pessoa["nascimento"], "%Y-%m-%d"),
            stack=pessoa["stack"],
        )

    return None


@dataclass
class Pessoa:
    id: uuid.UUID
    apelido: str
    nome: str
    nascimento: datetime
    stack: List[str]

    def __hash__(self) -> int:
        return self.id.int

    @staticmethod
    def build(data: dict) -> Self:
        if not isinstance(data.get("apelido"), str):
            raise TypeError('Esperava "str" para o campo "apelido"')
        elif not isinstance(data.get("nome"), str):
            raise TypeError('Esperava "str" para o campo "nome"')
        elif not isinstance(data.get("nascimento"), str) or not is_valid_date(
            data.get("nascimento")
        ):
            raise TypeError('Formato inesperado recebido no campo "data"')
        elif not isinstance(data.get("stack"), list) or not is_valid_stack(
            data.get("stack")
        ):
            raise TypeError('Formato inesperado recebido no campo "stack"')
        return Pessoa(
            id=uuid.uuid4(),
            nome=data.get("nome"),
            apelido=data.get("apelido"),
            nascimento=datetime.strptime(data.get("nascimento"), "%Y-%m-%d"),
            stack=data.get("stack"),
        )

    @staticmethod
    async def get_from_term(pool: Pool, termo: str) -> List[Self]:
        async with pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT
                    id,
                    nome,
                    apelido,
                    nascimento,
                    stack
                FROM t_pessoa
                WHERE
                    ts @@ to_tsquery('english', $1);
                """,
                termo,
            )

            if not records:
                return []

            pessoas = []
            for record in records:
                pessoas.append(
                    Pessoa(
                        id=record["id"],
                        nome=record["nome"],
                        apelido=record["apelido"],
                        nascimento=record["nascimento"],
                        stack=record["stack"].split(","),
                    )
                )
            return pessoas

    @staticmethod
    async def get(pool: Pool, pessoa_id: str) -> Self:
        # Checa no cache
        if pessoa := get_pessoa_from_cache(pessoa_id):
            return pessoa

        # Consome do banco
        async with pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                SELECT
                    id,
                    nome,
                    apelido,
                    nascimento,
                    stack
                FROM t_pessoa
                WHERE
                    id::text = $1
                """,
                pessoa_id,
            )

            return Pessoa(
                id=record["id"],
                nome=record["nome"],
                apelido=record["apelido"],
                nascimento=record["nascimento"],
                stack=record["stack"].split(","),
            )

    @staticmethod
    async def count(pool: Pool) -> int:
        async with pool.acquire() as conn:
            record = await conn.fetchrow(
                "SELECT row_count as count FROM row_count WHERE table_name = 't_pessoa'"
            )

            return record["count"]

    def as_dict(self) -> dict:
        return {
            "id": str(self.id),
            "nome": self.nome,
            "apelido": self.apelido,
            "nascimento": datetime.strftime(self.nascimento, "%Y-%m-%d"),
            "stack": self.stack,
        }

    async def save(self, pool: Pool):
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO t_pessoa (id, nome, apelido, nascimento, stack)
                VALUES
                    ($1, $2, $3, $4, $5)
            """,
                self.id,
                self.nome,
                self.apelido,
                self.nascimento,
                ",".join(self.stack),
            )
