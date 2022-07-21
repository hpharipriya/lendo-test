import json
from core import settings
import requests
#!/usr/bin/env python
import pika
import logging

logger = logging.getLogger(__name__)
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
    res = requests.post(api+"/api/applications", headers=headers, data=json.dumps(payload))
    logger.info("Bank API : " + api + " Responded " + str(res.status_code))
    return res.json() if res else None


def send_to_queue(obj_id, bank_name, bank_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(Q_URL))
    channel = connection.channel()
    channel.queue_declare(queue='status_checker')
    channel.basic_publish(exchange='',
                          routing_key='status_checker',
                          body=json.dumps({"uuid": str(obj_id), "bank_name": bank_name, "bank_id": bank_id}))
    print(" [x] Sent application id and bank APIs.")
    connection.close()
