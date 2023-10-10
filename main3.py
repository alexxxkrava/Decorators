import os
import requests
from functools import wraps
from datetime import datetime

def logger(log_file_path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            func_name = old_function.__name__
            result = old_function(*args, **kwargs)

            log_entry = f'{timestamp} - {func_name} -> {result}'

            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)

            return result

        return new_function

    return __logger

@logger('request_log.txt')  # Путь к файлу для логов
def req(url):
    response = requests.get(url)
    param = {}
    superhero = ['Hulk', 'Captain America', 'Thanos']
    for i in response.json():
        if i['name'] in superhero:
            param[i['name']] = i['powerstats']['intelligence']
    for key, val in param.items():
        if val == max(param.values()):
            return (f'Самый умный: {key} \nУровень интеллекта: {val}\n')
        if val == min(param.values()):
            return (f'Самый глупый: {key} \nУровень интеллекта: {val}\n')

if __name__ == '__main__':
    link = 'https://akabab.github.io/superhero-api/api//all.json'
    req(link)