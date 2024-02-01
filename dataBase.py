from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
from supabase import create_client
from funcoes import verificarConflitos,verificarConflitosEntreOProprioUser,verificarConflitosEntreOpropriouserParaEditar

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
            print(e)
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
        AgendamentosJaexistentes = self.visualizarAgendamentos(data)

        dados_de_novo_agendamento = {"data_agendamento" : [data],
                 "hora_inicio":[horaInicio],
                 "hora_fim":[horaFim],
                 "id": [id],
                 "Gestor":[gestor]}
        
        retornoFuncao = verificarConflitos(AgendamentosJaexistentes,dados_de_novo_agendamento)
        retornoFuncaoProprioUser = verificarConflitosEntreOProprioUser(AgendamentosJaexistentes,dados_de_novo_agendamento)
        if retornoFuncao == True or retornoFuncao == None:
            if retornoFuncaoProprioUser == True:
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
                return {"error": "Conflitos de horários entre o próprio usuário!",
                    "horario_inicio": retornoFuncaoProprioUser["horario_inicio"],
                    "horario_fim": retornoFuncaoProprioUser["horario_fim"]},400
        else:
            return {"error": "Conflitos de horários!",
                    "horario_inicio": retornoFuncao["horario_inicio"],
                    "horario_fim": retornoFuncao["horario_fim"]},400

    def editarAgendamento(self,dataAgendamento,horaInicio,horaFim,id,gestor,id_gestor):
        print(f'Estou dentro de Editar Agendamento')
        
        retorno = self.visualizarAgendamentos(dataAgendamento)
        print(f'Retorno dos já agendados{retorno}')
        
        retornoClasse = self.visualizarParaEditar(dataAgendamento,id_gestor)
        print(f'Retorno visualizar para Editar {retornoClasse}')
        
        novoAgendamentoEditado = {
                                    "data_agendamento":[dataAgendamento],
                                    "hora_inicio":[horaInicio],
                                    "hora_fim":[horaFim],
                                    "id": [id],
                                    "Gestor":[gestor],
                                    "id_gestor":[id_gestor]
                                }
        novoAgendamentoEditado02 = {
                                    "data_agendamento":[dataAgendamento],
                                    "hora_inicio":[horaInicio],
                                    "hora_fim":[horaFim],
                                    "Gestor":[gestor],
                                    "id":[id_gestor]
                                }
        
        print(f'Antes de entrar na função verificar Conflitos entre todos os users')
        retornoFuncao = verificarConflitos(retorno,novoAgendamentoEditado02)
        
        if retornoFuncao == True:
            pass
        else:
            print({"error": "Conflitos de horários!",
                    "horario_inicio": retornoFuncao["horario_inicio"],
                    "horario_fim": retornoFuncao["horario_fim"]})
            
            return {"error": "Conflitos de horários!",
                    "horario_inicio": retornoFuncao["horario_inicio"],
                    "horario_fim": retornoFuncao["horario_fim"]},400
            
        print(f'Depois de entrar na função verificar Conflitos entre todos os users')
        print(f'RETORNO verificar Conflitos entre todos os users: {retornoFuncao}')
        print(f'Antes de entrar na função verificar verificarConflitosEntreOpropriouserParaEditar')
        retornouser = verificarConflitosEntreOpropriouserParaEditar(retornoClasse,novoAgendamentoEditado)
        print(f'Depois de entrar na função verificar verificarConflitosEntreOpropriouserParaEditar')
        print(f'RETORNO verificarConflitosEntreOpropriouserParaEditar: {retornouser}')
        
        if retornoFuncao == True:
            if retornouser == True:
                try:
                    print(f'Dentro do Try para efetuar -----------------------UPDATE----------------------')
                    data, count = self.client.table('sala_de_reuniao').update({
                                "data_agendamento": dataAgendamento,
                                "hora_inicio": horaInicio,
                                "hora_fim": horaFim,
                            }).eq("id",id).execute()
                    print(f'DEU BOM Try para efetuar -----------------------UPDATE----------------------')
                except Exception as e:
                    error = e
                    print(f'ERRO Try para efetuar -----------------------UPDATE----------------------')
                    return {
                                "error": "Ocorreu um erro ao tentar realizar um cadastro no banco de dados",
                                "erro_apresentado": list(error)
                            }
                return {"sucess": "Editado com sucesso!"}, 200
            else:
                print({"error": "Conflitos de horários entre o próprio usuário!",
                    "horario_inicio": retornouser["horario_inicio"],
                    "horario_fim": retornouser["horario_fim"]})
                
                return {"error": "Conflitos de horários entre o próprio usuário!",
                    "horario_inicio": retornouser["horario_inicio"],
                    "horario_fim": retornouser["horario_fim"]},400
        else:
            return {"error": "Conflitos de horários!",
                    "horario_inicio": retornoFuncao["horario_inicio"],
                    "horario_fim": retornoFuncao["horario_fim"]},400
    
    def excluirAgendamento(self,id):
        try:
            data,count = self.client.table('sala_de_reuniao').delete().eq("id",id).execute()
        except Exception as e:
             return {"error": "ocorreu algum erro inesperado"},400
        return {"sucess": "Agendamento excluido com sucesso"},200
    
    def visualizarParaEditar(self,data,id):
        try:
            response,count = self.client.table('sala_de_reuniao').select('data_agendamento', 'hora_inicio', 'hora_fim', 'Gestor','id').eq('id_gestor',id).eq("data_agendamento",data).execute()
            response_string = response[1]
            resposta = json.loads(json.dumps(response_string))
            if resposta == []:
                 return {"error": f'Não há agendamentos para está data:'}
            return resposta
        except Exception as e:
            error = str(e)
            return {"error": f'Ocorreu algum erro: {error}'}

    def cadastrarColaborador(self,dados):
        nome = dados["nome"]
        cpf = dados["cpf"]
        nome_smart = dados["nome_smart"]
        cargo = dados["cargo"]
        data_nascimento = dados["data_nascimento"]
        telefone_pessoal = dados["telefone_pessoal"]
        horario_expediente = dados["horario_expediente"]
        regional = dados["regional"]
        data_admissao = dados["data_admissao"]
        coordenacao = dados["coordenacao"]
        id_gestor = dados["id_gestor"]

        try:
             response, count = self.client.table('funcionarios').insert({
                                                                            "cpf":cpf,"nome":nome,
                                                                            "nome_smartOmini":nome_smart,
                                                                            "cargo":cargo,"data_nascimento":data_nascimento,
                                                                            "telefone_pessoal":telefone_pessoal,
                                                                            "horario_expediente":horario_expediente,
                                                                            "regional":regional,"data_admissao":data_admissao,
                                                                            "coordenacao":coordenacao,"id_gestor":id_gestor
                                                                        }).execute()
        except Exception as e:
            error = str(e)
            print(f'Erro {error}')
            return {"error": "Erro no banco de dados:"}, 500
        return {"Sucess": "Colaborador cadastrado com sucesso:"},200
    
    def inserirFeedback(self,dados):
        motivo_macro = dados["motivo_macro"]
        motivoFeedback = dados["motivoFeedback"]
        nomeColaborador = dados["nomeColaborador"]
        id_gestor = dados["id_gestor"]
        pontos_abordados = dados["pontos_abordados"]

        try:
            response , count = self.client.table("feedbacks").insert({
                                                                        "motivo_macro":motivo_macro,
                                                                        "motivo":motivoFeedback,
                                                                        "texto_livre":pontos_abordados,
                                                                        "id_gestor":id_gestor,
                                                                        "Nome_colaborador":nomeColaborador
                                                                    }).execute()
            return {"Sucess": "Inserido no banco de dados com sucesso!"},200
        except Exception as e:
            error = str(e)
            return {f'error': f'{error}'}
        
    def visualizarFeedbacks(self,id):
        try:
            response, count = self.client.table("view_feedbacks").select("data_inserida","motivo_macro","motivo","nome_colaborador","nome_supervisor").eq("id_gestor",id).execute()
            response_string = response[1]
            resposta = json.loads(json.dumps(response_string))
            return resposta
        except Exception as e:
            error = str(e)
            return {f'error':f'{error}'}
    
    def inserirTicketSmart(self,dados):
        data_incidente = dados.ge["date"]
        num_ticket = dados.get["ticket"]
        hora_inicio = dados.get["hora_inicio"]
        hora_fim = dados.get["hora_fim"]
        normalizado = dados.get["normalizado"]
        motivo = dados.get["motivo"]
        id_gestor = dados.get["id"]
        nome_gestor = dados.get["nome_gestor"]
        try:
            response, count = self.client.table('ticket_smart').insert({
                "data_incidente":data_incidente,"num_ticket":num_ticket,"hora_inicio":hora_inicio,"hora_fim":hora_fim,
                "normalizado":normalizado,"motivo":motivo,"id_gestor":id_gestor,"nome_gestor":nome_gestor
            }).execute()
            return {"sucess":"dados inseridos com sucesso"},200
        except Exception as e:
            error = str(e)
            return{"error":error},400