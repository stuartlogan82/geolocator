import os
from flask import Flask, render_template, request, current_app, jsonify
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from twilio.rest import Client

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
TWILIO_SYNC_SERVICE_SID = os.environ.get('TWILIO_SYNC_MAP_SERVICE_SID')
TWILIO_API_KEY = os.environ.get('TWILIO_API_KEY')
TWILIO_API_SECRET = os.environ.get('TWILIO_API_SECRET')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', googleMapsApiKey=GOOGLE_MAPS_API_KEY)


@app.route('/<number>', methods=['GET', 'POST'])
def index_number(number):
    return render_template('index.html', googleMapsApiKey=GOOGLE_MAPS_API_KEY, identity=number)


@app.route('/dequeue', methods=['POST'])
def dequeue():
    print(request.is_json)
    content = request.get_json()
    print(content)
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    members = client.queues('QUb0d7407f6dc34f3cacc898794c164767').members.list()

    for record in members:
        print(record.call_sid)

    return jsonify('JSON posted'), 200


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
