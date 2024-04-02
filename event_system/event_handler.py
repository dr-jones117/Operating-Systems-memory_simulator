import heapq
from event_system.event import Event
from logger import Logger
from event_system.event_type import EventType
from memory_management.memory_manager import MemoryManager
from process_system.process import Process


class EventHandler:
    def __init__(self, logger: Logger, memory_manager: MemoryManager):
        self.logger = logger;
        self.current_time = None
        self.event_queue = []
        self.memory_manager = memory_manager
        self.first_time = True
        self.turnaround_calc = 0
        self.num_processes = 0

    def add_event(self, event: Event):
        heapq.heappush(self.event_queue, event)

    def allocate_process_to_memory_manager(self):
        process = self.memory_manager.allocate_process()
        if process != None:
            self.logger.log(f"MM moves Process {process.id} to memory\n\t")
            self.logger.log(self.memory_manager.get_memory_map_str())

            leave_event = Event(EventType.PROCESS_DEPARTURE, self.current_time + process.memory_lifetime, process)
            self.add_event(leave_event)

    def turnaround_time(self):
        return self.turnaround_calc / self.num_processes

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
                self.logger.log(f"Process {event.process.id} Arrives\n\t")
                
                self.memory_manager.add_process(event.process)
                insert_event = Event(EventType.ALLOCATE_PROCESS, self.current_time, event.process)
                self.add_event(insert_event)

                self.logger.log(f"Input Queue:{str(self.memory_manager.process_queue_str())}\n\t")

            elif event.type == EventType.PROCESS_DEPARTURE:
                self.logger.log(f"Process {event.process.id} completes\n\t")
                self.turnaround_calc += (self.current_time - event.process.arrival_time)
                
                self.memory_manager.deallocate_process(event.process)
                self.allocate_process_to_memory_manager()

                self.logger.log(self.memory_manager.get_memory_map_str())
                    

            elif event.type == EventType.ALLOCATE_PROCESS:
                self.allocate_process_to_memory_manager()

        self.logger.log(f"\nAverage Turnaround Time: {str(self.turnaround_time())}")

        
                    
