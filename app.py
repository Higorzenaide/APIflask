from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
from supabase import create_client
from dataBase import BancoDeDados

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("OUTRA_VARIAVEL")

app = Flask(__name__)

@app.route('/consultar/<senha>,<email>', methods=['GET'])
def hello(senha,email):
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.VerificaLogin(senha,email)
    return jsonify(retorno)

if __name__ == '__main__':
    app.run(debug=True)
