from os import supports_dir_fd
from flask import Blueprint, redirect, url_for, render_template, Response, request
import model

app: Blueprint = Blueprint(
    'home', __name__, url_prefix='/home'
)


def redirect_to_home() -> Response:
    endpoint = f'{app.name}.{__render_home.__name__}'
    return redirect(url_for(endpoint))


@app.route('/')
def __render_home() -> Response:
    if not model.session_manager.has_session():
        model.session_manager.create_session()
    sd: model.Novel2VecWrapper = model.session_manager.get_session_data()
    context = dict(
        initial_positive_titles_text=' '.join(sd.positive_titles),
        initial_negative_titles_text=' '.join(sd.negative_titles),
        similar_novels=sd.get_similar_novels(),
        any_unknown_titles=sd.any_unknown_titles(),
        unknown_titles=sd.get_unknown_titles(),
        search_query_is_empty=sd.is_search_query_empty(),

        search_url=url_for(f'{app.name}.{__search_novels.__name__}')
    )
    return render_template('home.html', **context)


@app.post('/search')
def __search_novels() -> Response:
    if not model.session_manager.has_session():
        model.session_manager.create_session()
    sd: model.Novel2VecWrapper = model.session_manager.get_session_data()
    sd.set_search_query(
        positive_titles=request.form['positive_titles_text'].split(),
        negative_titles=request.form['negative_titles_text'].split()
    )
    model.session_manager.set_session_data(sd)
    return redirect(url_for(f'{app.name}.{__render_home.__name__}'))
