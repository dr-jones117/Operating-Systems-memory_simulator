import heapq

from event_system.event import Event
from event_system.event_logger import EventLogger
from event_system.event_type import EventType


class EventHandler:
    def __init__(self, out_path: str):
        self.current_time = 0
        self.event_queue = []
        self.event_logger = EventLogger(out_path)

    def add_event(self, event: Event):
        heapq.heappush(self.event_queue, event)

    def run_events(self):
        while self.event_queue:
            event: Event = heapq.heappop(self.event_queue)
            if event.type == EventType.PROCESS_ARRIVAL:
                self.event_logger.log_event("\nProcess Arriving!")
            elif event.type == EventType.PROCESS_DEPARTURE:
                self.event_logger.log_event("Process Departing!")
            elif event.type == EventType.ATTEMPT_PROCESS_MEMORY_INSERT:
                self.event_logger.log_event("\nAttempt insert process into memory!")

            self.event_logger.log_event(str(event))