# rinha backend

Projeto baseado na
[Rinha de Backend Edição 2023](https://github.com/zanfranceschi/rinha-de-backend-2023-q3/blob/main/INSTRUCOES.md).

Este projeto tem o objetivo de testar possibilidades de otimização de forma a, a
cada versão nova, reduzir o tempo médio de requisições por segundo tanto nas
rotas de consulta quanto de inserção de dados.

A cada versão nova, [este changelog](CHANGELOG.md) será atualizado com os
resultados obtidos.

## Instruções para execução

Este projeto precisa basicamente do Docker/Docker Compose para executar. Na HOME
do projeto, execute:

```sh
docker-compose up
```

A API responderá na porta :8000

## Instruções para testar a performance

Junto do projeto, está configurado também um script que pode ser executado com a
ajuda do [Locust](https://locust.io/), na pasta `loadtest/`. Com a ferramenta
devidamente instalada, execute:

```sh
locust -f loadtest/load_all_routes.py
```

A partir daí é possível acessar a interface da ferramenta e configurar um teste
de carga.
