from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
from supabase import create_client
from moldes.dataBase import create_client

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("OUTRA_VARIAVEL")

app = Flask(__name__)

@app.route('/consultar/<id>', methods=['GET', 'POST'])
def hello(id):
    instanciar_teste = create_client()
    retorno = instanciar_teste.visualizarDados(id)
    return jsonify(retorno)

if __name__ == '__main__':
    app.run(debug=True)
