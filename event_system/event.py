from event_system.event_type import *
from process_system.process import Process

class Event:
    def __init__(self, type: EventType, time: int, process: Process):
        self.type = type
        self.time = time
        self.process = process

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        return f"Event type: {self.type}, Time: {self.time}, Process: {self.process.id}"
