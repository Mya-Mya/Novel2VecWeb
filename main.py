from presenters import home
from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import timedelta
from argparse import ArgumentParser

app: Flask = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=1)
with open('SECRET_KEY.txt', 'r') as file:
    app.secret_key = file.read()
app.register_blueprint(home.app)


@app.route('/')
def __require_redirect_to_home() -> Response:
    return home.redirect_to_home()


if __name__ == '__main__':
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    if args.debug:
        app.run('0.0.0.0', 8000, True)
    else:
        app.run()
