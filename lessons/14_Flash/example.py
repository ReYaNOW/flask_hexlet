from flask import (
    Flask,
    flash,
    url_for,
    request,
    redirect,
    get_flashed_messages,
    render_template,
)
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
app.secret_key = 'secret_key'


@app.route('/')
def hello_world():
    return 'Hello, Hexlet!'


@app.route('/users')
def get_users():
    with open('db.json') as db_file:
        users = json.loads(db_file.read())
    
    search = request.args.get('term', '')
    
    for user in users:
        print(user['name'])
    if search:
        term = search.lower()
        filtered_users = [
            user for user in users if term in user['name'].lower()
        ]
    else:
        filtered_users = users
    
    messages = get_flashed_messages(with_categories=True)
    if messages:
        print(messages)
    
    return render_template(
        'users/index.html',
        search=search,
        users=filtered_users,
        messages=messages,
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
        return (
            render_template(
                'users/new.html',  # noqa
                user=user,
                errors=errors,
            ),
            422,
        )
    
    user['id'] = random.randint(1, 1000)  # noqa
    users.append(user)
    flash('User was added successfully', 'success')
    
    with open('db.json', 'w') as db_file:
        db_file.write(json.dumps(users))
    
    return redirect(url_for('get_users'), code=302)
