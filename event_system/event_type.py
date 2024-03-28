from enum import Enum

class EventType(Enum):
    PROCESS_ARRIVAL = 1
    PROCESS_DEPARTURE = 2
    ATTEMPT_PROCESS_MEMORY_INSERT = 3