import heapq
from event_system.event import Event
from event_system.event_type import EventType
from logging_system.logger import Logger
from memory_management.memory_manager import MemoryManager


class EventHandler:
    def __init__(self, logger: Logger, memory_manager: MemoryManager):
        self.logger = logger;
        self.memory_manager = memory_manager

        self.entry_counter = 0
        self.event_queue = []

        self.current_time = None
        self.first_time = True

        self.turnaround_calc = 0
        self.num_processes = 0

    def add_event(self, event: Event):
        event.entry_order = self.entry_counter
        self.entry_counter += 1
        heapq.heappush(self.event_queue, event)

    def allocate_processes_to_memory(self):
        process = self.memory_manager.allocate_process()
        while(process != None):
            self.logger.log(f"MM moves Process {process.id} to memory\n\t")
            self.logger.log(f"Input Queue:{self.memory_manager.get_process_queue_str()}\n\t")

            self.logger.log(self.memory_manager.get_memory_map_str())

            leave_event = Event(EventType.PROCESS_DEPARTURE, self.current_time + process.memory_lifetime, process)
            self.add_event(leave_event)

            process = self.memory_manager.allocate_process()

    def turnaround_time(self):
        return round(self.turnaround_calc / self.num_processes, 2)

    def run_events(self):
        while self.event_queue:
            event: Event = heapq.heappop(self.event_queue)

            if self.current_time != event.time:
                if self.first_time:
                    self.logger.log(f"t = {event.time}: ")
                    self.first_time = False
                else:
                    self.logger.log(f"\nt = {event.time}: ")
                
                self.current_time = event.time

            if event.type == EventType.PROCESS_ARRIVAL:
                self.num_processes += 1
                self.logger.log(f"Process {event.process.id} arrives\n\t")
                
                self.memory_manager.add_process(event.process)
                insert_event = Event(EventType.ALLOCATE_PROCESS, self.current_time)
                self.add_event(insert_event)

                self.logger.log(f"Input Queue:{self.memory_manager.get_process_queue_str()}\n\t")

            elif event.type == EventType.PROCESS_DEPARTURE:
                self.logger.log(f"Process {event.process.id} completes\n\t")
                
                self.memory_manager.deallocate_process(event.process)
                self.logger.log(self.memory_manager.get_memory_map_str())

                insert_event = Event(EventType.ALLOCATE_PROCESS, self.current_time)
                self.add_event(insert_event)   

                self.turnaround_calc += (self.current_time - event.process.arrival_time)     

            elif event.type == EventType.ALLOCATE_PROCESS:
                self.allocate_processes_to_memory()

        self.logger.log(f"\nAverage Turnaround Time: {str(self.turnaround_time())}\n")

        
                    
