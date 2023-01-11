from pathlib import Path
from datetime import datetime


class Logger:
    def __init__(self, log_file, error_log_file) -> None:
        self.__log_file = log_file
        self.__error_log_file = error_log_file
        self.__create_log_file(self.__log_file)
        self.__create_log_file(self.__error_log_file)

    def __create_log_file(self, file):
        path = Path(file)
        if not path.is_file():
            with open(file, 'w'):
                pass

    def print_log(self, content, level):
        print(content)

    def write_log(self, content, level):
        with open(self.__log_file, 'a') as log_file:
            log_file.write(content + "\n")
        if level == 2:
            with open(self.__error_log_file, 'a') as error_log:
                error_log.write(content + "\n")

    def log(self, content, level=0):
        time = datetime.now().strftime('%d.%m.%Y %H:%M')
        pre_content = '[LOG]    - '
        if level == 2:
            pre_content = '[ERROR]  - '
        elif level == 1:
            pre_content = '[WARN]   - '

        content = pre_content + f"{time}: " + content
        self.print_log(content, level)
        self.write_log(content, level)

