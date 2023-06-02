from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient
from random import randint
from bson import json_util

application = Flask(__name__)
CORS(application)  # Habilitar CORS localmente

#aws documentDB
#client = MongoClient("mongodb://bancodm:leo180678@docdb-2023-05-29-14-28-59.cluster-cigoyjjdczx5.us-east-2.docdb.amazonaws.com:27017/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false")
client = MongoClient("mongodb+srv://bancodm:<password>@cluster0.ooxmyc5.mongodb.net/")

db = client["mongodm"]
pedidos = db["pedidos"]

#função para gerar o score
def scoreGen():
    return randint(1, 999)

@application.route("/", methods=['GET'])
def healthcheck():
    return {'status da api': 'ok'}

#rota para listar os pedidos
@application.route("/listAll", methods=['GET'])
def listAll():
    pedido_list = list(pedidos.find())
    return json_util.dumps({'pedidos': pedido_list})

#rota para deletar pedidos
@application.route("/deletePedido/<cpf>", methods=['DELETE'])
def deletePedido(cpf):
    pedidos.delete_one({'cpf': cpf})
    return {'status': 'pedido deletado'}

from bson import json_util

#rota para inserir pedido
@application.route("/insertPedido", methods=['POST'])
def insertPedido():
    data = request.get_json()
    cpf = data.get("cpf")
    nome = data.get("nome")
    email = data.get("email")
    renda = data.get("renda")
    
    # Se renda for None, seta como 0.0
    renda = float(renda) if renda is not None else 0.0

    #função pra gerar score e atribuir o result
    score = scoreGen()

    if 1 <= score <= 299:
        status = "REPROVADO"
        limite = 0
    elif 300 <= score <= 599:
        status = "APROVADO"
        limite = 1000
    elif 600 <= score <= 799:
        status = "APROVADO"
        limite = renda / 2
        if limite < 1000:
            limite = 1000
    elif 800 <= score <= 950:
        status = "APROVADO"
        limite = renda * 2
    elif 951 <= score <= 999:
        status = "APROVADO"
        limite = 1000000

    #inserir pedido no mongoDB
    pedido = {"cpf": cpf, "nome": nome, "email": email, "renda": renda, "score": score, "limite": limite, "status": status}
    pedidos.insert_one(pedido)

    # Consulta o pedido recém-inserido para pegar os dados completos
    inserted_pedido = pedidos.find_one({"cpf": cpf})

    # Converte o ObjectId em uma representação serializável
    inserted_pedido['_id'] = str(inserted_pedido['_id'])

    return {'pedido': json_util.dumps(inserted_pedido)}



if __name__ == "__main__":
    application.run(port=5000, debug=True)
