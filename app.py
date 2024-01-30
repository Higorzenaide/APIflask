from flask import Flask,jsonify,request
from dataBase import BancoDeDados  # Certifique-se de que esta importação está correta
from datetime import datetime
app = Flask(__name__)

@app.route('/ConsultarLogin', methods=['GET'])
def consultar():
    data = request.json
    email = data.get("email")
    senha = data.get("senha")
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.VerificaLogin(senha, email)
    return jsonify(retorno)

@app.route('/FazerCadastro', methods=['POST'])
def efetuarCadastro():
    data = request.json
    nome = data.get("nome")
    email = data.get("email")
    matricula = data.get("matricula")
    senha = data.get("senha")
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.cadastrar(nome, email, matricula, senha)
    return jsonify(retorno)

@app.route('/VisualizarAgendamentos/<data>', methods=['GET'])
def visualizarAgendamentosDoDia(data):
    data_formatada = datetime.strptime(data, "%Y-%m-%d")
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.visualizarAgendamentos(data_formatada)
    return jsonify(retorno)

@app.route('/FazerAgendamento',methods = ['POST'])
def fazerAgendamento():
    data = request.json
    dataAgendamento = data.get("data_agendamento")
    horaInicio = data.get("hora_inicio")
    horaFim = data.get("hora_fim")
    id = data.get("id")
    gestor = data.get("Gestor")
    instanciarBanco = BancoDeDados()
    retorno = instanciarBanco.efetuarAgendamento(dataAgendamento,horaInicio,horaFim,id,gestor)
    return jsonify(retorno)

@app.route('/EditarAgendamento',methods = ['POST'])
def editarAgendamento():
    data = request.json
    dataAgendamento = data.get("data_agendamento")
    horaInicio = data.get("hora_inicio")
    horaFim = data.get("hora_fim")
    id = data.get("id")
    id = int(id)
    gestor = data.get("Gestor")
    id_gestor = data.get("id_gestor")
    instanciarBanco = BancoDeDados()
    retorno = instanciarBanco.editarAgendamento(dataAgendamento,horaInicio,horaFim,id,gestor,id_gestor)
    return jsonify(retorno)

@app.route('/ExcluirAgendamento', methods = ['POST'])
def excluirAgendamento():
    data = request.json
    id = data.get("id")
    instanciaBanco = BancoDeDados()
    retorno = instanciaBanco.excluirAgendamento(id)
    return jsonify(retorno)

@app.route('/VisualizarParaEditar',methods = ['GET'])
def VisualizarParaEditar():
    data = request.json
    id = data.get("id")
    data = data.get("data_agendamento")
    instanciarBanco = BancoDeDados()
    retorno = instanciarBanco.visualizarParaEditar(data,id)
    return jsonify(retorno)


@app.route('/CadastrarColaborador', methods = ['POST'])
def cadastrarColaborador():
    data = request.json
    cpf = data.get("cpf")
    nome = data.get("nome")
    nome_smartOmini = data.get("nome_smartOmini")
    cargo = data.get("cargo")
    data_nascimento = data.get("data_nascimento")
    telefone_pessoal = data.get("telefone_pessoal")
    horario_expediente = data.get("horario_expediente")
    regional = data.get("regional")
    data_admissao = data.get("data_admissao")
    coordenacao = data.get("coordenacao")
    id_gestor = data.get("id_gestor")

    dados = {"cpf":cpf,
             "nome":nome,
             "nome_smart":nome_smartOmini,
             "cargo":cargo,
             "data_nascimento":data_nascimento,
             "telefone_pessoal":telefone_pessoal,
             "horario_expediente":horario_expediente,
             "regional":regional,
             "data_admissao":data_admissao,
             "coordenacao":coordenacao,
             "id_gestor":id_gestor}
    
    instanciarBanco = BancoDeDados()
    retorno = instanciarBanco.cadastrarColaborador(dados)
    return jsonify(retorno)

@app.route('/InserirFeedback', methods = ['POST'])
def inserirFeedback():
    data = request.json
    motivoMacro = data.get("motivo_macro")
    motivoFeedback = data.get("motivo")
    nomeColaborador = data.get("Nome_colaborador")
    id_gestor = data.get("id_gestor")
    pontos_abordados = data.get("pontos")  

    dadosFeddback = {
        "motivo_macro":motivoMacro,
        "motivoFeedback":motivoFeedback,
        "nomeColaborador":nomeColaborador,
        "id_gestor":id_gestor,
        "pontos_abordados":pontos_abordados
    }

    instaciarBanco = BancoDeDados()
    retorno = instaciarBanco.inserirFeedback(dadosFeddback)
    return jsonify(retorno)

@app.route('/VisualizarFeedbacks', methods = ['GET'])
def visualizarFeedbacks():
    data = request.json
    id = data.get("id")
    instaciarBanco = BancoDeDados()
    retorno = instaciarBanco.visualizarFeedbacks(id)
    return jsonify(retorno)

if __name__ == '__main__':
    app.run(debug=True)
