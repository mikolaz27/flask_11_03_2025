from flask import Flask

app = Flask(__name__)

@app.route("/admin")
def hello_world_admin():
    return "<p>Hello, Admin!!!</p>"


@app.route("/")
def hello_world():
    return "<p>Hello, Mykhailo!!!</p>"


# https://flask.palletsprojects.com:443/en/stable/quickstart#1
# https | http
# SSL
#
# c -> r1 -> r2 -> r3 -> r4 -> s5
#            |
#           check data
#
# flask.palletsprojects.com
# domain
# DNS
# Василь робота -> 067-564-98-74
# Іванка перехмахер -> 067-564-98-73
# Петро сусід -> 067-564-98-71
#
# flask.palletsprojects.com -> 104.16.254.120
# facebook.com -> 57.144.110.1


# 443 - https
# 80 - http
# 22 - ssh
# 5432 - database (postgres)
# 8000 -

# en/stable/quickstart
#1

if __name__ == '__main__':
    app.run(
        'localhost', debug=True
    )