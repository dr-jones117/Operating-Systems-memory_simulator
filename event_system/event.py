from event_system.event_type import *
from process_system.process import Process

class Event:
    def __init__(self, type: EventType, time: int, process: Process = None):
        self.type = type
        self.time = time
        self.process = process
        self.entry_order = None

    def __lt__(self, other):
        if self.time < other.time:
            return True
        elif self.time == other.time:
            if self.type == EventType.PROCESS_ARRIVAL and other.type == EventType.ALLOCATE_PROCESS:
                return True
            elif self.type == EventType.PROCESS_DEPARTURE and other.type == EventType.ALLOCATE_PROCESS:
                return True
            elif self.type == EventType.ALLOCATE_PROCESS and other.type != EventType.ALLOCATE_PROCESS:
                return False
            elif self.entry_order < other.entry_order:
                return True
        return False
            

    def __str__(self):
        return f"Event type: {self.type}, Time: {self.time}, Process: {self.process.id}"
