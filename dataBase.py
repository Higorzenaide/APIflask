from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
from supabase import create_client
from datetime import datetime

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

            if resposta == []:
                return {"error": "E-mail ou senha invalidos"}, 400
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
            return {"Sucess": "Cadastro efetuado com sucesso"}, 200
        except Exception as e:
            error_message = str(e)
                    # Verifica se a mensagem de erro indica uma violação de chave única
            if 'duplicate key value violates unique constraint "users_email_key"' in error_message:
                        return {"error": "E-mail já cadastrado. Por favor, use outro e-mail."}, 400
            else:
                        print(f"Erro durante o cadastro: {error_message}")
                        return {"error": "Erro durante o cadastro"}, 400

    def visualizarAgendamentos(self, data):
        try:
            response = self.client.table('sala_de_reuniao').select({
                "data_agendamento", "hora_inicio", "hora_fim", "Gestor"
            }).eq('data_agendamento', data).execute()
            print('Passou01')
            response_string = response[1]
            print('Passou02')
            resposta = json.loads(json.dumps(response_string))
            print('Passou03')
            return resposta
        
        except Exception as e:
            error = str(e)
            return {"error": f'Ocorreu algum erro: {error}'}
            
        