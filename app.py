from flask import Flask,jsonify,request
from dataBase import BancoDeDados  # Certifique-se de que esta importação está correta

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

@app.route('/VisualizarAgendamentos/<data>',methods=['GET'])
def visualizarAgendamentosDoDia(data):
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.visualizarAgendamentos(data)
    return jsonify


if __name__ == '__main__':
    app.run(debug=True)
