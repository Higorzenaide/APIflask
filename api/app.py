from flask import Flask
from dotenv import load_dotenv
import os

class Teste:
    def __init__(self) -> None:
        pass

    def testeHello(self):
        return 'helloWorld'

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

api_key = os.getenv("API_KEY")
outra_variavel = os.getenv("OUTRA_VARIAVEL")

app = Flask(__name__)

@app.route('/')
def hello():
    instanciar_teste = Teste()
    retorno = instanciar_teste.testeHello()
    return retorno

if __name__ == '__main__':
    app.run(debug=True)
