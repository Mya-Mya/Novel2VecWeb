from presenters import home
from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import timedelta

app: Flask = Flask(__name__)
app.permanent_session_lifetime=timedelta(minutes=1)
app.secret_key='as/3/rrd-4_tn3o.i4.'
app.register_blueprint(home.app)


@app.route('/')
def __require_redirect_to_home() -> Response:
    return home.redirect_to_home()


if __name__ == '__main__':
    app.run()
