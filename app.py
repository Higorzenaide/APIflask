from flask import Flask,jsonify,request
from dataBase import BancoDeDados  # Certifique-se de que esta importação está correta

app = Flask(__name__)

@app.route('/ConsultarLogin/<senha>/<email>', methods=['GET'])
def consultar(senha, email):
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.VerificaLogin(senha, email)
    return jsonify(retorno)

@app.route('/FazerCadastro', methods=['POST'])
def efetuarCadastro():
    data = request.json  # Assume que os dados são enviados como JSON no corpo da solicitação
    nome = data.get("nome")
    email = data.get("email")
    matricula = data.get("matricula")
    senha = data.get("senha")

    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.cadastrar(nome, email, matricula, senha)
    return jsonify(retorno)

if __name__ == '__main__':
    app.run(debug=True)
