import random

from faker import Faker
from flask import Flask, jsonify, request

SEED = 1234


def generate_companies(companies_count):
    fake = Faker()
    fake.seed_instance(SEED)
    ids = list(range(companies_count))
    random.seed(SEED)
    random.shuffle(ids)
    companies = []
    for i in range(companies_count):
        companies.append(
            {'name': fake.company(), 'phone': fake.phone_number()}
        )
    return companies


companies = generate_companies(10)

app = Flask(__name__)


@app.route('/')
def index():
    return "<a href='/companies'>Companies</a>"


# BEGIN (write your solution here)
@app.route('/companies')
def get_companies():
    page_num = request.args.get('page', default=1, type=int)
    per_num = request.args.get('per', default=5, type=int)
    
    start_ind = (page_num - 1) * per_num
    result = companies[start_ind: page_num * per_num]
    return jsonify(result)
# END
