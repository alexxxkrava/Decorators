import os
from functools import wraps
from datetime import datetime

def logger(log_file_path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            func_name = old_function.__name__
            args_str = ', '.join([f'{key}={value}' for key, value in kwargs.items()] + [str(arg) for arg in args])
            result = old_function(*args, **kwargs)

            log_entry = f'{timestamp} - {func_name}({args_str}) -> {result}\n'

            with open(log_file_path, 'a') as log_file:
                log_file.write(log_entry)

            return result

        return new_function

    return __logger

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

if __name__ == '__main__':
    test_2()