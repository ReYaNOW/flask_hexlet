from flask import Flask

# Это callable WSGI-приложение
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Hexlet!'


@app.post('/users')
def users():
    return 'Users', 302


@app.post('/users')
def users_post():
    return 'POST /users'
