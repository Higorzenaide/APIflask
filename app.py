from flask import Flask,jsonify
from dataBase import BancoDeDados  # Certifique-se de que esta importação está correta

app = Flask(__name__)

@app.route('/ConsultarLogin/<senha>/<email>', methods=['GET'])
def consultar(senha, email):
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.VerificaLogin(senha, email)
    return jsonify(retorno)

@app.route('/FazerCadastro/<nome>/<email>/<int:matricula>/<senha>', methods=['POST'])
def efetuarCadastro(nome,email,matricula,senha):
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.cadastrar(nome,email,matricula,senha)
    return jsonify({"status": "Cadastro efetuado com sucesso"})

if __name__ == '__main__':
    app.run(debug=True)
