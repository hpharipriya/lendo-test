#!/usr/bin/env python
import pika, sys, os
import json
import requests

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='status_checker')
    def call_status_check_on_bank_api(body):
        headers = {
            'Content-Type': 'application/json',
            'Accept': '/*/'
        }
        json_body = json.loads(body)
        print("body", body)
        print("json body", json_body)
        bank_url = "http://"+json_body.get("bank")+":8000/api/jobs?application_id="+json_body.get("uuid")
        res = requests.get(bank_url, headers=headers)
        print("------ res--------", res.json())
        data = res.json()
        data.get("application_id")
        data.get("status")


        ## call partial update
        app_id = data.get("application_id")

        url = "http://django_backend:8000/customer/api/app/"+app_id+"/"
        payload = {
            "bank": json_body.get("bank"),
            "status": data.get("status"),
        }
        print("===========")
        print(url)
        print("88888888888")

        res = requests.patch(url, headers=headers, data=json.dumps(payload))
        test_url = 'curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://django_backend:8000/customer/api/app/6a1cd076-4d31-4c22-9799-20d85bd1579f/'


        print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        print(res.status_code)
        data = res.json()
        print(data)



    def callback(ch, method, properties, body):
        print(" [x] Received application details: %r" % body)
        print("calling API")
        call_status_check_on_bank_api(body)

    channel.basic_consume(queue='status_checker', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)