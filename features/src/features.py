from datetime import datetime
import json
from time import sleep

import numpy as np
import pika
from sklearn.datasets import load_diabetes


# np.random.seed(42)
i = 0
while True:
    try:
        X, y = load_diabetes(return_X_y=True)
        random_row = np.random.randint(0, X.shape[0]-1)
# print(y.shape, y.dtype, random_row.dtype)

        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        channel.queue_declare(queue='y_true')    
        messID = datetime.timestamp(datetime.now())
        y_true = {'id': messID, 'body': float(y[random_row])}
        features = {'id': messID, 'body': list(X[random_row])}
        channel.basic_publish(exchange='', routing_key='y_true', body=json.dumps(y_true))
        print('Сообщение с правильным ответом отправлено в очередь')

        channel.queue_declare(queue='features')
        channel.basic_publish(exchange='', routing_key='features', body=json.dumps(features))
        print('Сообщение с вектором признаков отправлено в очередь')

        connection.close()
    except Exception as e:
        print('Не удалось подключиться к очереди')
        print(e.__class__.__name__, e)
    finally:
        sleep(5)
   
