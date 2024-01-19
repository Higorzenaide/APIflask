from flask import Flask
from dotenv import load_dotenv
import os
class teste:
    def __init__(self) -> None:
        pass

    def testeHeloo(self):
        return 'helloWorld'
    
api_key = os.getenv("API_KEY")
outra_variavel = os.getenv("OUTRA_VARIAVEL")

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)


@app.route('/')
def hello():
    instanciarteste = teste()
    retorno = instanciarteste.testeHeloo
    return retorno

if __name__ == '__main__':
    app.run(debug=True)
