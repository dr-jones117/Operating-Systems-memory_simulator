from enum import Enum

class EventType(Enum):
    PROCESS_ARRIVAL = 1
    PROCESS_DEPARTURE = 2
    ALLOCATE_PROCESS = 3