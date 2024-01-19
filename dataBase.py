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
      
    def VerificaLogin(self,senha,email):
        try:
            response, data = self.client.table('users').select('id','Gestor','email','verificado','supervisao','treinamentos').eq('senha',senha).eq('email',email).execute()
            response_string = response[1]
            resposta = json.loads(json.dumps(response_string))
            return resposta
        except Exception as e:
            return e
    
    def cadastrar(self, nome, email, matricula, senha):
        try:
            response, count = self.client.table('users').insert({
                "Gestor": nome,
                "matricula": matricula,
                "senha": senha,
                "email": email,
                "verificado": False,
                "supervisao": False,
                "treinamentos": False
            }).execute()

            # Verifica se a inserção foi bem-sucedida
            if count > 0:
                return {"status": "Cadastro efetuado com sucesso"}
            else:
                return {"error": "Erro durante o cadastro"}

        except Exception as e:
            app.logger.error(f"Erro durante o cadastro: {str(e)}")
            return {"error": "Erro durante o cadastro"}, 400

        
        