from typing import TextIO

class EventLogger:
    def __init__(self, path: str):
        try:
            self.out_file: TextIO = open(path, 'w')
            self.current_time = 0
        except FileNotFoundError:
            print("Error: File not found:", path)
            exit(1)
    
    def log_event(self, log: str):
        self.out_file.write(log)