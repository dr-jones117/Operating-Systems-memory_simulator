from logging_system.logger import Logger


class ConsoleLogger(Logger):
    def log(self, log: str):
        print(log, end='')