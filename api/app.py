from flask import Flask
class hello:
    def __init__(self):
        return 'hello'

app = Flask(__name__)

@app.route('/')
def hello():
    ola = hello()
    return ola

if __name__ == '__main__':
    app.run(debug=True)
