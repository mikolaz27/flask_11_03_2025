import pprint
import string

import httpx

from random import choices
from http import HTTPStatus

from flask import Flask, request, jsonify, Response
from webargs.flaskparser import use_kwargs

from database_handler import execute_query
from validator import password_length_validator

app = Flask(__name__)


@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handling(error):
    headers = error.data.get("headers", None)
    messages = error.data.get("messages", ["Invalid request."])

    if headers:
        return jsonify(
            {"errors": messages},
            error.code,
            headers
        )

    return jsonify(
        {"errors": messages},
        error.code
    )


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

    if result.status_code not in (HTTPStatus.OK,):
        return Response("ERROR: Something went wrong with api.open-notify.org",
                        status=result.status_code)

    result: dict = result.json()
    statistics = {}
    for entry in result.get('people', []):
        statistics[entry['craft']] = statistics.get(entry['craft'], 0) + 1

    pprint.pprint(result)

    return statistics


@app.route("/get-customers")
def get_all_customers():
    query = "SELECT FirstName, LastName FROM customers"

    records = execute_query(query=query)
    return records


if __name__ == '__main__':
    app.run(
        'localhost', debug=True
    )

# 100 - info
# 200 - OK
# 300 - redirect
# 400 - client
# 500 - server

# GET - get info
# params in url
# search/filter

# POST - change on server
# has request body
# passwords/data/files/

# SQL -

# relation !- SQL

# no relation !- SQL
