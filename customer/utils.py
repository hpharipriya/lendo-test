import json
from core import settings
import requests
#!/usr/bin/env python
import pika

Q_URL = settings.Q_URL

def call_bank_apis(api, app):
    headers = {
        'Content-Type': 'application/json',
        'Accept': '/*/'
    }

    payload = {
        "id": str(app.uuid),
        "first_name": app.first_name,
        "last_name": app.last_name
    }
    print("===========")
    print(api)
    print("88888888888")
    res = requests.post(api+"/api/applications", headers=headers, data=json.dumps(payload))

    print(res.status_code)
    data = res.json()
    print(data)
    return data


def send_to_queue(obj_id, bank_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(Q_URL))
    channel = connection.channel()
    channel.queue_declare(queue='status_checker')
    channel.basic_publish(exchange='',
                          routing_key='status_checker',
                          body=json.dumps({"uuid": str(obj_id), "bank": bank_name}))
    print(" [x] Sent application id and bank APIs.")
    connection.close()

# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#
# channel.basic_consume(queue='hello',
#                       auto_ack=True,
#                       on_message_callback=callback)