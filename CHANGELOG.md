# Melhorias implementadas

## Primeira versão

A primeira versão do projeto funciona como um base line para entender a
performance da app sem grandes mudanças de arquitetura. Todas as requisições
nessa versão vão direto no banco.

As seguintes otimizações feitas:

- Ajuste da configuração padrão do PostgreSQL considerando os limites de RAM
  estabelecidos. Feito com ajuda do [PGTune](https://pgtune.leopard.in.ua/).

- Ajuste na configuração do NGINX para ter um tempo de keepalive definido e
  manter algumas conexões entre o NGINX e o backend.

[Resultado do teste de carga da primeira versão](https://htmlpreview.github.io/?https://raw.githubusercontent.com/desk467/rinha-backend-23/main/reports/primeira_versao.html)

## Segunda versão

Nesta versão, o objetivo foi implementar a seguinte otimização:

- Ajustar a criação de uma Pessoa de forma bufferizada, acumulando algumas
  inserções antes de enviar para o banco de dados

[Resultado do teste de carga da segunda versão](https://htmlpreview.github.io/?https://raw.githubusercontent.com/desk467/rinha-backend-23/main/reports/segunda_versao.html)

## Terceira versão

- Ajusta consulta de Pessoa para primariamente usar um cache em memória,
  atualizado via pg notify/liste

- Ajusta consulta de contagem de pessoas para usar uma tabela auxiliar,
  preenchida com trigger

- Ajusta consulta de pessoas por termo de busca para usar ts vector do Postgres
  (Full Text Search)

[Resultado do teste de carga da terceira versão](https://htmlpreview.github.io/?https://raw.githubusercontent.com/desk467/rinha-backend-23/main/reports/terceira_versao.html)
