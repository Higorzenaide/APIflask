from flask import Flask
from dotenv import load_dotenv
import os

api_key = os.getenv("API_KEY")
outra_variavel = os.getenv("OUTRA_VARIAVEL")
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/')
def hello():
    return 'api_key'

if __name__ == '__main__':
    app.run(debug=True)
