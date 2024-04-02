import heapq
from event_system.event import Event
from logger import Logger
from event_system.event_type import EventType
from memory_management.memory_manager import MemoryManager


class EventHandler:
    def __init__(self, logger: Logger, memory_manager: MemoryManager):
        self.logger = logger;
        self.current_time = None
        self.event_queue = []
        self.memory_manager = memory_manager

    def add_event(self, event: Event):
        heapq.heappush(self.event_queue, event)

    def run_events(self):
        while self.event_queue:
            event: Event = heapq.heappop(self.event_queue)

            if self.current_time != event.time:
                self.logger.log(f"\n\nNew Time! {event.time}")
                self.current_time = event.time

            if event.type == EventType.PROCESS_ARRIVAL:
                self.logger.log("\nProcess Arriving!")
                insert_event = Event(EventType.ATTEMPT_PROCESS_MEMORY_INSERT, 
                                     self.current_time, 
                                     event.process, 
                                     self.memory_manager)
                self.add_event(insert_event)

            elif event.type == EventType.PROCESS_DEPARTURE:
                self.logger.log("Process Departing!")

            elif event.type == EventType.ATTEMPT_PROCESS_MEMORY_INSERT:
                self.logger.log(f"\nAttempt insert process into memory!  {event.process}")