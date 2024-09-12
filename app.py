import subprocess
from datetime import datetime
import requests
from authlib.integrations.flask_client import OAuth
from dotenv import dotenv_values
from flask import Flask, render_template, url_for, session, redirect, request
from werkzeug.middleware.proxy_fix import ProxyFix

config = dotenv_values(".env")

app = Flask(__name__)
app.secret_key = config.get("APP_SECRET_KEY")
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERRED_URL_SCHEME'] = 'https'
oauth = OAuth(app)

google = oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=config.get('CLIENT_ID'),
    client_secret=config.get('CLIENT_SECRET'),
    client_kwargs={
        'scope': 'openid email'
    }
)


@app.route('/')
def index():
    return render_template('index.html', session=session)


@app.route('/update', methods=['POST'])
def update_currency_rates():
    result = process_form_data(request.form)
    if result:
        update_from, update_to = result
        update_google_sheets(update_from, update_to)
    return redirect(url_for('index'))


def process_form_data(request_form):
    update_from, update_to = None, None

    try:
        date_format = '%Y-%m-%d'
        update_from = datetime.strptime(request_form.get('update from'), date_format)
        update_to = datetime.strptime(request_form.get('update to'), date_format)
    except ValueError as err:
        session['update result'] = f'Invalid input: {err}'

    if update_from is None or update_to is None:
        session['update result'] = '"update from" and "update to" fields must not be empty'
    elif update_from > update_to:
        session['update result'] = f'"update from" field must be earlier than "update to"'
    else:
        session['update result'] = f'Updated for {update_from} to {update_to}'
        return update_from, update_to

    return None


def update_google_sheets(update_from, update_to):
    update_from = update_from.strftime('%Y%m%d')
    update_to = update_to.strftime('%Y%m%d')
    url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={update_from}&end={update_to}&valcode=usd&sort=exchangedate&order=desc&json'
    response = requests.get(url).text

    try:
        subprocess.check_call(['python', 'updater.py', response])
    except subprocess.CalledProcessError:
        session['update result'] = 'Something went wrong while updating spreadsheet information'


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    google = oauth.create_client('google')
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    print(token)
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
