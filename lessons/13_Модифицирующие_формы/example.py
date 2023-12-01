from flask import Flask, render_template, request, redirect, url_for
import json
import random


def validate_user(user):
    errors = {}
    if not user.get('name'):
        errors['name'] = 'cant be blank'
    if not user.get('email'):
        errors['email'] = 'cant be blank'
    return errors


# Это callable WSGI-приложение
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Hexlet!'


@app.route('/users')
def get_users():
    with open('db.json') as db_file:
        users = json.loads(db_file.read())

    return render_template(
        'users/index.html', # noqa
        users=users,
    )


@app.route('/users/new')
def users_new():
    user = {'name': '', 'email': ''}
    errors = {}

    return render_template('users/new.html', user=user, errors=errors)  # noqa


@app.post('/users')
def users_post():
    with open('db.json') as db_file:
        users = json.loads(db_file.read())

    user = request.form.to_dict()
    errors = validate_user(user)
    if errors:
        return render_template(
            'users/new.html',  # noqa
            user=user,
            errors=errors,
        ), 422
    
    user['id'] = random.randint(1, 1000) # noqa
    users.append(user)

    with open('db.json', 'w') as db_file:
        db_file.write(json.dumps(users))

    return redirect(url_for('get_users'), code=302)
