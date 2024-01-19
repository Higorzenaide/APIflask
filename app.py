from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
from supabase import create_client

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("OUTRA_VARIAVEL")

class BancoDeDados:
    def __init__(self):
        self.client = create_client(DATABASE_URL, API_KEY)
      
    def visualizarDados(self, id):
        response, data = self.client.table('feedbacks').select('motivo_macro', 'motivo', 'Nome_colaborador', 'date').eq('id_gestor', id).execute()
        response_string = response[1]
        resposta = json.loads(json.dumps(response_string))
        return resposta

app = Flask(__name__)

@app.route('/consultar/<id>', methods=['GET', 'POST'])
def hello(id):
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.visualizarDados(id)
    return jsonify(retorno)

if __name__ == '__main__':
    app.run(debug=True)
