# Documentação da API Flask - Desafio DM

Essa é a documentação para uma API Flask simples que realiza operações CRUD com "pedidos" em um banco de dados MongoDB.

A aplicação utiliza as seguintes bibliotecas: Flask, flask_cors, pymongo, random e bson.

As configurações iniciais incluem a criação da aplicação Flask e habilitação de CORS para permitir o acesso a partir de origens diferentes. O aplicativo então se conecta ao MongoDB através do MongoClient com um link de conexão específico e seleciona a base de dados "mongodm" e a coleção "pedidos".

# Rotas
A aplicação possui as seguintes rotas:

# GET /
Rota de verificação de saúde da API, retorna o status da API.

GET /

Resposta:

{
    "status da api": "ok"
}

# GET /listAll
Esta rota lista todos os pedidos existentes no banco de dados.

GET /listAll

Resposta:

{
    "pedidos": [
        {
            // detalhes do pedido 1
        },
        {
            // detalhes do pedido 2
        },
        // ...
    ]
}

# DELETE /deletePedido/{cpf}
Esta rota deleta um pedido específico baseado no CPF fornecido.

DELETE /deletePedido/{cpf}

Resposta:

{
    "status": "pedido deletado"
}

# POST /insertPedido
Esta rota insere um novo pedido no banco de dados. Ele aceita dados no formato JSON no corpo da solicitação com os seguintes campos: cpf, nome, email, renda. Ele calcula o "score" usando um método de geração de números aleatórios e, com base no score, atribui um status e limite.

POST /insertPedido

Corpo da solicitação:

{
    "cpf": "12345678901",
    "nome": "John Doe",
    "email": "john.doe@example.com",
    "renda": "5000.0"
}

Resposta:

{
    "pedido": {
        "_id": "606bc83eb428ec5a8f9a96ce",
        "cpf": "12345678901",
        "nome": "John Doe",
        "email": "john.doe@example.com",
        "renda": 5000.0,
        "score": 567,
        "limite": 2500.0,
        "status": "APROVADO"
    }
}


