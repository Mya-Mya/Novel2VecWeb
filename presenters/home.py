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
        initial_positive_titles_text=' '.join(sd.sq.positive),
        initial_negative_titles_text=' '.join(sd.sq.negative),
        similar_novels=sd.get_similar_novels(),
        any_unknown_titles=sd.any_unknown_titles(),
        unknown_titles=sd.get_unknown_titles(),
        search_query_is_empty=sd.sq.is_empty(),

        search_url=url_for(f'{app.name}.{__search_novels.__name__}')
    )
    return render_template('home.html', **context)


@app.post('/search')
def __search_novels() -> Response:
    if not model.session_manager.has_session():
        model.session_manager.create_session()
    sd: model.Novel2VecWrapper = model.session_manager.get_session_data()

    sq: model.SearchQuery = model.SearchQuery(
        positive=request.form['positive_titles_text'].split(),
        negative=request.form['negative_titles_text'].split(),
    )

    sd.set_search_query(sq)
    return redirect(url_for(f'{app.name}.{__render_home.__name__}'))
