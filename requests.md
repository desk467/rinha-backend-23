# Create Pessoa

```sh
curl -X POST http://localhost:8000/pessoas -H 'Content-Type: application/json' -d  '{"nome":"João Ricardo","apelido":"rics","nascimento":"1996-02-15","stack":["ruby","golang","javascript"]}' -v

curl -X POST http://localhost:8000/pessoas -H 'Content-Type: application/json' -d  '{"nome":"José Roberto","apelido":"joseph","nascimento":"1998-04-12","stack":["ruby","golang","javascript"]}' -v
```

# Get Pessoa

```sh
curl -X GET http://localhost:8000/pessoas/pessoa_id -v
```

# Get Pessoa from Termo

curl -X GET http://localhost:8000/pessoas?t=python -v

# Get Contagem Pessoas

curl -X GET http://localhost:8000/contagem-pessoas -v
