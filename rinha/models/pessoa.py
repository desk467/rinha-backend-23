import uuid
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Self
from asyncpg import Pool
from rinha.util import dump_terms


def is_valid_date(date_as_str) -> bool:
    try:
        datetime.strptime(date_as_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_stack(stack) -> bool:
    return all(isinstance(item, str) for item in stack)


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
    async def generate_table(pool: Pool):
        async with pool.acquire() as connection:
            await connection.execute(
                """
                    CREATE TABLE IF NOT EXISTS t_pessoa (
                        id uuid PRIMARY KEY,
                        nome varchar(120) NOT NULL,
                        apelido varchar(50) NOT NULL,
                        nascimento date NOT NULL,
                        stack jsonb NOT NULL,
                        termos text
                    )
                """
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
                    termos ILIKE $1
                """,
                f"%{termo}%",
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
                        stack=json.loads(record["stack"]),
                    )
                )
            return pessoas

    @staticmethod
    async def get(pool: Pool, pessoa_id: str) -> Self:
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
                stack=json.loads(record["stack"]),
            )

    @staticmethod
    async def count(pool: Pool) -> int:
        async with pool.acquire() as conn:
            record = await conn.fetchrow("SELECT count(1) as count FROM t_pessoa")

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
                INSERT INTO t_pessoa (id, nome, apelido, nascimento, stack, termos)
                VALUES
                    ($1, $2, $3, $4, $5, $6)
            """,
                self.id,
                self.nome,
                self.apelido,
                self.nascimento,
                json.dumps(self.stack),
                dump_terms(self.nome, self.apelido, self.stack),
            )
