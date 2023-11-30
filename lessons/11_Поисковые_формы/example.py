from flask import Flask, render_template, request

users = ['mike', 'mishel', 'adel', 'keks', 'kamila']

# Это callable WSGI-приложение
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Hexlet!'


@app.route('/users')
def get_users():
    search = request.args.get('term', '')
    
    if search:
        term = search.lower()
        filtered_users = [user for user in users if term in user]
    else:
        filtered_users = users

    return render_template(
        'users/index.html',
        search=search,
        users=filtered_users,
    )
