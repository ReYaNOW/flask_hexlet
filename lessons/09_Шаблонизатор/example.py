from flask import Flask, render_template

# Это callable WSGI-приложение
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Hexlet!'


# @app.route('/users/<id_>')
# def users(id_):
#     return render_template(
#         'index.html',
#         name=id_,
#     )

@app.route('/users/<id_>')
def users(id_):
    return render_template(
        'users/show.html',
        name=id_,
    )
