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



if __name__ == '__main__':
    app.run(debug=True)
