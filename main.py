import pprint
import string

import httpx

from random import choices
from http import HTTPStatus

from flask import Flask, request
from webargs.flaskparser import use_kwargs
from webargs import validate, fields

from database_handler import execute_query
from validator import password_length_validator

app = Flask(__name__)


@app.route("/admin")
def hello_world_admin():
    return "<p>Hello, Admin!!!</p>"


@app.route("/")
def hello_world():
    return "<p>Hello, Mykhailo!!!</p>"


@app.route("/generate-password")
@use_kwargs(
    password_length_validator,
    location="query"
)
def generate_password(length):
    # password_length = request.args.get("length", default="10")
    #
    # if not password_length.isdigit():
    #     return "ERROR: length should be a number!"
    #
    # password_length = int(password_length)
    #
    # if not 8 <= password_length <= 100:
    #     return "ERROR: password length should be in range: [8, 100]"

    # GET
    #  - get info
    #  - in url path
    #  - search, filter
    # POST
    #  - change info
    #  - with body
    #  - for secure data (password, credit cards ...), files,

    password = "".join(
        choices(string.digits + string.ascii_letters + string.punctuation, k=length)
    )
    return f"Generated password: {password}"

@app.route("/get-astronauts")
def get_astronauts():
    url = "http://api.open-notify.org/astros.json"
    result = httpx.get(url=url, params={})

    if result.status_code not in (HTTPStatus.OK, ):
        return "ERROR: Something went wrong with api.open-notify.org"

    result: dict = result.json()
    statistics = { }
    for entry in result.get('people', []):
        statistics[entry['craft']] = statistics.get(entry['craft'], 0) + 1

    pprint.pprint(result)

    return statistics



@app.route("/get-customers")
@use_kwargs(
    {
        "first_name": fields.Str(
           required=True,
        ),
         "last_name": fields.Str(
           load_default=None,
        ),
    },
    location="query"
)
def get_all_customers(first_name, last_name):
    # TODO: I will need it later when task 023 will be available
    query = "SELECT FirstName, LastName FROM customers"

    fields = {}

    if first_name:
        fields['FirstName'] = first_name
    if last_name:
        fields['LastName'] = last_name

    if fields:

        # create where condition for query using accumulation of fields
        query += " WHERE " + " AND ".join(
            f"{key}=?" for key in fields
        )

    print(query)
    records = execute_query(query=query, args=tuple(fields.values()))
    return records


if __name__ == '__main__':
    app.run(
        'localhost', debug=True
    )
