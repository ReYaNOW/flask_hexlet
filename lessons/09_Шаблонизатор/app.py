from flask import Flask, render_template

from data import generate_users

users = generate_users(100)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# BEGIN (write your solution here)
@app.route('/users')
def get_all_users_info():
    return render_template('users/index.html', users=users)


@app.route('/users/<int:id_>')
def get_user_info(id_):
    for user in users:
        if id_ == user['id']:
            return render_template('users/show.html', user=user)
    return 'Page not found', 404


# END
