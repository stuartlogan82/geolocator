import os
from flask import Flask, render_template, request, current_app, jsonify
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
TWILIO_SYNC_SERVICE_SID = os.environ.get('TWILIO_SYNC_MAP_SERVICE_SID')
TWILIO_API_KEY = os.environ.get('TWILIO_API_KEY')
TWILIO_API_SECRET = os.environ.get('TWILIO_API_KEY_SECRET')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', googleMapsApiKey=GOOGLE_MAPS_API_KEY)


@app.route('/<number>', methods=['GET', 'POST'])
def index_number(number):
    return render_template('index.html', googleMapsApiKey=GOOGLE_MAPS_API_KEY, identity=number)


@app.route('/token')
def token():
    # get the userid from the incoming request
    identity = request.values.get('identity', None)
    # Create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID,
                        TWILIO_API_KEY,
                        TWILIO_API_SECRET, identity=identity)
    # Create a Sync grant and add to token
    sync_grant = SyncGrant(
        service_sid=TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant)
    # Return token info as JSON
    return jsonify(identity=identity, token=token.to_jwt().decode('utf-8'))


if __name__ == '__main__':
    app.run()
