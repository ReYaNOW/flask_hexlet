from flask import (
    Flask,
    flash,
    url_for,
    request,
    redirect,
    get_flashed_messages,
    render_template,
    make_response,
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


@app.get('/users')
def get_users():
    # with open('db.json') as db_file:
    #     users = json.loads(db_file.read())

    users = request.cookies.get('users')
    if not users:
        users = '[]'
    users = json.loads(users)

    search = request.args.get('term', '')

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
    # with open('db.json') as db_file:
    #     users = json.loads(db_file.read())

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
    users = request.cookies.get('users')
    if not users:
        users = '[]'
    users = json.loads(users)

    user['id'] = random.randint(1, 1000)  # noqa
    users.append(user)
    flash('User was added successfully', 'success')

    encoded_users = json.dumps(users)
    response = make_response(redirect(url_for('get_users'), code=302))
    response.set_cookie('users', encoded_users)
    print(response)
    # with open('db.json', 'w') as db_file:
    #     db_file.write(json.dumps(users))

    return response


@app.route('/users/<int:id_>')
def get_user(id_):
    users = request.cookies.get('users')
    if not users:
        users = '[]'
    users = json.loads(users)
    # with open('db.json') as db_file:
    #     users = json.loads(db_file.read())

    for user in users:
        if id_ == user['id']:
            return render_template('users/user.html', user=user)  # noqa

    else:
        return 'Page not found', 404


@app.route('/users/<int:id_>/edit')
def edit_user(id_):
    # with open('db.json') as db_file:
    #     users = json.loads(db_file.read())

    users = request.cookies.get('users')
    if not users:
        users = '[]'
    users = json.loads(users)

    for user in users:
        if id_ == user['id']:
            errors = []
            return render_template(
                'users/edit.html', user=user, errors=errors  # noqa
            )

    else:
        return 'Page not found', 404


@app.post('/users/<int:id_>')
def user_post(id_):
    # with open('db.json') as db_file:
    #     users = json.loads(db_file.read())

    users = request.cookies.get('users')
    if not users:
        users = '[]'
    users = json.loads(users)

    updated_user = request.form.to_dict()
    errors = validate_user(updated_user)
    if errors:
        return (
            render_template(
                'users/new.html',  # noqa
                user=updated_user,
                errors=errors,
            ),
            422,
        )
    print(id_, type(id_))
    for i, user in enumerate(users):
        if id_ == user['id']:
            users[i].update(updated_user)
            flash('User was updated successfully', 'success')

            # with open('db.json', 'w') as db_file:
            #     db_file.write(json.dumps(users))

            encoded_users = json.dumps(users)
            response = make_response(
                redirect(url_for('get_user', id_=id_), code=302)
            )
            response.set_cookie('users', encoded_users)
            return response

        return redirect(url_for('get_user', id_=id_), code=302)

    return 'Page not found', 404


@app.route('/users/<int:id_>/delete', methods=['POST'])
def delete_user(id_):
    # with open('db.json') as db_file:
    #     users = json.loads(db_file.read())

    users = request.cookies.get('users')
    if not users:
        users = '[]'
    users = json.loads(users)

    for i, user in enumerate(users):
        if id_ == user['id']:
            users.pop(i)
            # with open('db.json', 'w') as db_file:
            #     db_file.write(json.dumps(users))

            encoded_users = json.dumps(users)
            response = make_response(redirect(url_for('get_users')))
            response.set_cookie('users', encoded_users)
            return response

    flash('User has been deleted', 'success')
    return redirect(url_for('get_users'))
