from urllib.parse import urljoin

import requests

BASE_URL = 'http://localhost:8000'


def test_users():
    response = requests.get(urljoin(BASE_URL, '/users'))
    assert 'Stephanie' in response.text
    assert 'Maria' in response.text
    assert 'Shelly' in response.text
    assert 'href="/users/4' in response.text


def test_user1():
    response = requests.get(urljoin(BASE_URL, '/users/4'))
    assert 'Andres' in response.text
    assert 'Cox' in response.text
    assert 'wyoung@gmail.com' in response.text


def test_user2():
    response = requests.get(urljoin(BASE_URL, '/users/51'))
    assert 'Brian' in response.text
    assert 'Rich' in response.text
    assert 'fhall@gmail.com' in response.text


def test_user3():
    response = requests.get(urljoin(BASE_URL, '/users/82'))
    assert 'Matthew' in response.text
    assert 'Petty' in response.text
    assert 'respinoza@gmail.com' in response.text


def test_user_not_found():
    response = requests.get(urljoin(BASE_URL, '/users/100'))
    assert response.text == 'Page not found'
    assert response.status_code == 404


if __name__ == '__main__':
    test_users()
    test_user1()
    test_user2()
    test_user3()
    test_user_not_found()
    