from flask import Blueprint, request, redirect, url_for, session, jsonify, render_template, make_response
from flask.ext.login import login_user, logout_user
from werkzeug.security import gen_salt
from datetime import datetime, timedelta

from pasteur.extensions import cache, oauth
from pasteur.forms import LoginForm
from pasteur.models import db, User, Grant, Token, Client

main = Blueprint('main', __name__)


@main.route('/api')
@cache.cached(timeout=1000)
def home():
    return "Pasteur API root."


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print("Form is valid")
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)
        oauth_client = Client.query.filter_by(user_id=user.id).first()
        if not oauth_client:
            item = Client(
                client_id=gen_salt(40),
                client_secret=gen_salt(50),
                _redirect_uris=' '.join([
                    'http://localhost:8000/authorized',
                    'http://127.0.0.1:8000/authorized',
                    'http://127.0.1:8000/authorized',
                    'http://127.1:8000/authorized',
                ]),
                _default_scopes='email',
                user_id=user.id,
            )
            db.session.add(item)
            db.session.commit()

        response = make_response(redirect("http://localhost:8000/callback"))
        response.set_cookie('client_id', oauth_client.client_id)
        response.set_cookie('client_secret', oauth_client.client_secret)
        return response
    return render_template("login.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    return "Logout success."

def current_user():
    if 'user_id' in session:
        uid = session['user_id']
        return User.query.get(uid)
    return None

@main.route('/client')
def client():
    user = current_user()
    if not user:
        return redirect('/login')
    item = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=' '.join([
            'http://localhost:8000/authorized',
            'http://127.0.0.1:8000/authorized',
            'http://127.0.1:8000/authorized',
            'http://127.1:8000/authorized',
        ]),
        _default_scopes='email',
        user_id=user.id,
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(
        client_id=item.client_id,
        client_secret=item.client_secret,
    )


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=current_user(),
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@main.route('/oauth/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None


@main.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user()
    if not user:
        return redirect('/')
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = user
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@main.route('/api/me')
@oauth.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.username)
