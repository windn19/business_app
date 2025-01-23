import csv
import json
import os

import pika
  

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='y_true')
    print('Подключено к каналу результатов')
    channel.queue_declare(queue='y_pred')
    print('Подключено к каналу предсказаний')
    result = dict()
    
    def callback(ch, method, properties, body):
        print(f'Из очереди {method.routing_key} получено значение {json.loads(body)}')
        meth = method.routing_key
        mess = json.loads(body)
        mess_id = mess['id']
        mess_body = mess['body']
        if mess_id not in result:
            result[mess_id] = {meth: mess_body}
        else:
            dict1 = result.pop(mess_id)
            key1, value1 = dict1.popitem()
            os.makedirs('logs', exist_ok=True)
            if not os.path.exists('logs/metric_log.csv'):
                with open('logs/metric_log.csv', mode='w', newline='', encoding='utf8') as f:
                    writer = csv.DictWriter(f, fieldnames=['id', key1, meth, 'absolute_error'])
                    writer.writeheader()
            with open('logs/metric_log.csv', mode='a', newline='', encoding='utf8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', key1, meth, 'absolute_error'])
                writer.writerow({'id': str(mess_id), key1: str(value1), meth: str(mess_body), 'absolute_error': abs(value1-mess_body)})
            
        

    channel.basic_consume(queue='y_true', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='y_pred', on_message_callback=callback, auto_ack=True)

    print('...Ожидаем сообщений, для выхода нажмите CTRL+C...')
    channel.start_consuming()
except Exception as e:
    print('Не удалось подключиться к очереди')
    print(e.__class__.__name__, e, e.__traceback__())
    
