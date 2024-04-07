from typing import TextIO
from logging_system.logger import Logger


class FileLogger(Logger):
    def __init__(self, path: str):
        try:
            self.out_file: TextIO = open(path, 'w')
        except FileNotFoundError:
            print("Error: File not found:", path)
            exit(1)
    
    def log(self, log: str):
        self.out_file.write(log)