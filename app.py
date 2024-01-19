from flask import Flask
from dataBase import BancoDeDados  # Certifique-se de que esta importação está correta

app = Flask(__name__)

@app.route('/consultar/<senha>/<email>', methods=['GET'])
def consultar(senha, email):
    # Suponho que você tenha uma função VerificaLogin no seu BancoDeDados
    # Certifique-se de que a classe BancoDeDados e a função VerificaLogin estejam corretamente definidas
    instanciar_teste = BancoDeDados()
    retorno = instanciar_teste.VerificaLogin(senha, email)
    return retorno

if __name__ == '__main__':
    app.run(debug=True)
