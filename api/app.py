from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello():
    return 'testando se está merda ta funfando'

if __name__ == '__main__':
    app.run(debug=True)
