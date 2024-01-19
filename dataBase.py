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
      
    def VerificaLogin(self, senha, email):
        try:
            response, data = self.client.table('users').select('id', 'Gestor', 'email', 'verificado', 'supervisao', 'treinamentos').eq('senha', senha, 'email', email).execute()
            
            # Verifique se a operação foi bem-sucedida antes de prosseguir
            if response.status_code == 200:
                response_string = response[1]
                resposta = json.loads(json.dumps(response_string))
                return {"success": True, "data": resposta}
            else:
                return {"success": False, "error": "Falha na consulta ao banco de dados"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        