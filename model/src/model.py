import json
import pickle

import numpy as np
import pika


with open('myfile.pkl', mode='rb') as f:
    regressor = pickle.load(f)

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='features')
    print('Подключено к каналу свойств')
    channel.queue_declare(queue='y_pred')
    print('Подключено к каналу предсказаний')
    
    def callback(ch, method, propreties, body):
        arr = json.loads(body)
        messID = arr['id']
        features = arr['body']
        print(f'Получен вектор признаков {features}')
        
        shaped_features = np.array(features).reshape(1, -1)
        pred = regressor.predict(shaped_features)[0]
        
        pred = {'id': messID, 'body': float(pred)}
        channel.basic_publish(exchange='', routing_key='y_pred', body=json.dumps(pred))
        print(f'Предсказание {pred} отправлено в очередь y_pred')
        
    channel.basic_consume(queue='features', on_message_callback=callback, auto_ack=True)
    print('...Ожидание сообщений. Для выхода нажмите CTRL+C...')

    channel.start_consuming()
except Exception as e:
    print('Не удалось подключиться к очереди')
    print(e.__class__.__name__, e)
