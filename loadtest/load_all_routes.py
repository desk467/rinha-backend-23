from random import choice, randint, sample
from datetime import datetime
from locust import HttpUser, task


langs = ["golang", "python", "ruby", "javascript", "lua", "cpp"]


def generate_valid_date():
    while True:
        try:
            date_str = f"{randint(1950, 2023)}-{str(randint(1,12)).zfill(2)}-{str(randint(1,30)).zfill(2)}"
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            pass


class LoadAllRoutes(HttpUser):
    @task
    def call_all_routes(self):
        nomes = [
            "José",
            "Carlos",
            "Maria",
            "Pedro",
            "João",
            "Claudia",
            "Amaurílio",
            "Ricardo",
            "Ana",
        ]

        sobrenomes = [
            "Gomes",
            "Sampaio",
            "Bragança",
            "Júnior",
            "Delgado",
            "Correa",
            "Abreu",
            "Silva",
            "Cruz",
            "Santos",
            "Lobo",
        ]

        nome = f"{choice(nomes)} {choice(sobrenomes)}"
        nascimento = generate_valid_date()
        pessoa = {
            "nome": nome,
            "apelido": nome.split(" ")[0].lower(),
            "nascimento": nascimento,
            "stack": sample(langs, 3),
        }

        response = self.client.post("/pessoas", json=pessoa)

        next_req_url = response.headers.get("Location")
        self.client.get(next_req_url, name="/pessoas/[pessoa_id]")
        self.client.get(f"/pessoas?t={choice(langs)}", name="/pessoas?t=[term]")
        self.client.get("/contagem-pessoas")
