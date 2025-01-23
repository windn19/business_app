import csv
import os
from time import sleep

from matplotlib import pyplot as plt
import seaborn as sns

if os.path.exists('./logs/metric_log.csv'):
    while True:
        try:
            with open('./logs/metric_log.csv', newline='') as f:
                data = list(csv.reader(f))
                
            result = [float(item[-1]) for item in data[1:]]

            plt.figure(figsize=(14, 10))
            sns_plot = sns.histplot(result, kde=True, bins=10)
            plt.savefig('./logs/error_distribution.png')
            plt.close()
            
        except Exception as e:
            print(f'Ошибка:', e.__class__.__name__, e, e.__traceback__())
        finally:
            sleep(5)

