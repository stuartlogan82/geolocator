import os
import json
from flask import Flask, render_template, request, current_app, jsonify, Response
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
TWILIO_SYNC_SERVICE_SID = os.environ.get('TWILIO_SYNC_SERVICE_SID')
TWILIO_API_KEY = os.environ.get('TWILIO_API_KEY')
TWILIO_API_SECRET = os.environ.get('TWILIO_API_SECRET')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
SERVICE_BASE_URL = os.environ.get('SERVICE_BASE_URL')

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
    # identity = content.get("identity")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call_sid = ''
    members = client.queues(
        'QU0273e99cff8753d81cc9912099ad0c01').members.list()

    calls = client.calls.list(status='in-progress')

    for record in calls:
        if record.from_ == '+{}'.format(content["identity"]):
            print(record.sid, record.from_)
            call_sid = record.sid

    for record in members:
        if record.call_sid == call_sid:
            print("found call!!", record.call_sid)
            member = client.queues('QU0273e99cff8753d81cc9912099ad0c01') \
                .members(call_sid) \
                .update(url='https://{}/enqueue_to_flex'.format(SERVICE_BASE_URL), method='GET',)
            print(member.call_sid)
            return jsonify({'message': 'Dequeued succesfully!'}), 200

    return jsonify({'message': 'Dequeue failed'}), 200


@app.route('/enqueue_to_flex')
def enqueue_to_flex():
    caller = request.args.get('Caller')
    formatted_caller = caller[1:]
    print(formatted_caller)
    location = fetch_sync_data(formatted_caller)
    print(location)
    resp = VoiceResponse()
    enqueue = resp.enqueue(
        None, workflow_sid='WW753b6e8c074d797802e6e68cc823b74d')
    enqueue.task(json.dumps(
        {'type': 'inbound', 'name': caller, 'lat': location['lat'], 'lng': location['lng']}))
    resp.append(enqueue)

    return str(resp)


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


def fetch_sync_data(unique_name):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    documents = client.sync.services(TWILIO_SYNC_SERVICE_SID) \
        .documents \
        .list()

    for record in documents:
        print(record)
        if unique_name == record.unique_name:
            document = client.sync.services(TWILIO_SYNC_SERVICE_SID) \
                .documents(unique_name) \
                .fetch()
            return document.data
        else:
            return {'lat': 0, 'lng': 0}


if __name__ == '__main__':
    app.run()
