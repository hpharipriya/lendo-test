#!/usr/bin/env python
import pika, sys, os
import json
import requests
import psycopg2
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

conn = psycopg2.connect(
    host=env('DB_HOST'),
    database=env('DB_NAME'),
    user=env('DB_USER'),
    password=env('DB_PASS'))

Q_URL = env('Q_URL')
FINAL_RESPONSES = ["completed", "rejected"]


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Q_URL))
    channel = connection.channel()
    channel.queue_declare(queue='status_checker')

    def update_status(status, bank_id, bank_name, app_id):
        print("Updating DB status" + status + " for " + bank_name)
        if status not in FINAL_RESPONSES:
            print("Status not in final status list. Sending to queue again")
            send_to_queue(app_id, bank_name, bank_id)
        else:
            cur = conn.cursor()
            cur.execute("update customer_bankapplication "
                        "set status='" + status +
                        "' where bank_id = " + str(bank_id) + " and application_id='"+str(app_id) + "' ")
            updated_rows = cur.rowcount
            print("Updated" + str(updated_rows) + " rows")
            conn.commit()
            cur.close()

    def send_to_queue(obj_id, bank_name, bank_id):
        channel.basic_publish(exchange='',
                              routing_key='status_checker',
                              body=json.dumps({"uuid": str(obj_id), "bank_name": bank_name, "bank_id": str(bank_id)}))
        print(" [x] Sent application id and bank APIs.")

    def call_status_check_on_bank_api(body):
        headers = {
            'Content-Type': 'application/json',
            'Accept': '/*/'
        }
        json_body = json.loads(body)
        bank_url = "http://"+json_body.get("bank_name")+":8000/api/jobs?application_id="+json_body.get("uuid")
        res = requests.get(bank_url, headers=headers)
        data = res.json()
        app_id = data.get("application_id")
        # url = "http://django_backend:8000/customer/api/app/"+app_id+"/"
        # payload = {
        #     "bank": json_body.get("bank"),
        #     "status": data.get("status"),
        # }
        # # res = requests.patch(url, headers=headers, data=json.dumps(payload))
        # test_url = 'curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://django_backend:8000/customer/api/app/6a1cd076-4d31-4c22-9799-20d85bd1579f/'
        #
        # print(res.status_code)
        # data = res.json()
        # print(data)
        status = data.get("status")
        bank_id = json_body.get("bank_id")
        bank_name = json_body.get("bank_name")
        update_status(status, bank_id, bank_name, app_id)

    def callback(ch, method, properties, body):
        print(" [x] Received application details: %r" % body)
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
