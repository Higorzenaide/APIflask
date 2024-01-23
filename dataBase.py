from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
from supabase import create_client
from funcoes import verificarConflitos

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
            if response_string == []:
                return {"error": "E-mail ou senha invalidos"}, 400
            return response_string
        except Exception as e:
            error_msg = str(e)
            return {'Ocorreu um erro inesperado, tente novamente, ou contate os administradores.', error_msg},500
    
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
            response, data = self.client.table('sala_de_reuniao').select('data_agendamento', 'hora_inicio', 'hora_fim', 'Gestor', 'created_at','id_gestor').eq('data_agendamento', data).execute()
            # Converter a resposta para um DataFrame do pandas
            response_string = response[1]
            resposta = json.loads(json.dumps(response_string))
            if resposta == []:
                 return {"error": f'Não há agendamentos para está data:'}
            return resposta
        except Exception as e:
            error = str(e)
            return {"error": f'Ocorreu algum erro: {error}'}
            
    def efetuarAgendamento(self,data,horaInicio,horaFim,id,gestor):
        retorno = self.visualizarAgendamentos(data)

        dados_de_novo_agendamento = {"data_agendamento" : [data],
                 "hora_inicio":[horaInicio],
                 "hora_fim":[horaFim],
                 "id": [id],
                 "Gestor":[gestor]}
        
        retornoFuncao = verificarConflitos(retorno,dados_de_novo_agendamento)

        if retornoFuncao == True:
            try:
                data, count = self.client.table('sala_de_reuniao').insert({
                            "data_agendamento": data,
                            "hora_inicio": horaInicio,
                            "hora_fim": horaFim,
                            "id_gestor": id,
                            "Gestor": gestor
                        }).execute()
            except Exception as e:
                error = e
                return{"error":"Ocorreu um erro ao tentar realizar um cadastro no banco de dados","erro apresentado": {error}}
            return {"sucess": "Agendado com sucesso!"}, 200
        else:
            return {"error": "Conflitos de horários!",
                    "horario_inicio": retornoFuncao["horario_inicio"],
                    "horario_fim": retornoFuncao["horario_fim"]},400

    def editarAgendamento(self,dataAgendamento,horaInicio,horaFim,id,gestor):
        retornoClasse = self.visualizarAgendamentos(dataAgendamento)

        novoAgendamentoEditado = {
                                    "data_agendamento":[dataAgendamento],
                                    "hora_inicio":[horaInicio],
                                    "hora_fim":[horaInicio],
                                    "id": [id],
                                    "Gestor":[gestor]
                                }
        
        retornoFuncao = verificarConflitos(retornoClasse,novoAgendamentoEditado)

        if retornoFuncao == True:
            try:
                data, count = self.client.table('sala_de_reuniao').update({
                            "data_agendamento": data,
                            "hora_inicio": horaInicio,
                            "hora_fim": horaFim,
                            "id_gestor": id,
                            "Gestor": gestor
                        }).eq("id",id).execute()
            except Exception as e:
                error = e
                return {
                            "error": "Ocorreu um erro ao tentar realizar um cadastro no banco de dados",
                            "erro_apresentado": list(error)
                        }
            return {"sucess": "Editado com sucesso!"}, 200
        else:
            return {"error": "Conflitos de horários!",
                    "horario_inicio": retornoFuncao["horario_inicio"],
                    "horario_fim": retornoFuncao["horario_fim"]},400
