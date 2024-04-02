from typing import List
from event_system.event import Event
from logger import Logger
from event_system.event_type import *
from process_system.process import Process
from process_system.process_file import ProcessFile
from memory_management.memory_manager import MemoryManager
from memory_management.memory_policy import MemoryPolicy
from event_system.event_handler import EventHandler

def main():
    mem_size: int = input('Memory Size: ') # represented in kBs
    policy: int = input('Memory management policy (1 - VSP, 2 - PAG, 3 - SEG): ')
    page_size: int = 0
    algorithm: int = 0
    
    if policy == MemoryPolicy.PAG:
        page_size = input('Page/Frame Size: ')
    else:
        algorithm = input('Fit algorithm (1 - first-fit, 2 - best-fit, 3 - worst-fit): ')

    path: str = input('Process Information File Name: ')
    out_path: str = input('Output File Name: ')

    process_file: ProcessFile = ProcessFile(path)
    processes: List[Process] = process_file.get_processes()
    logger = Logger(out_path)

    memory_manager: MemoryManager = MemoryManager(logger, mem_size, page_size)
    event_handler = EventHandler(logger, memory_manager)
    
    for process in processes:
        event = Event(EventType.PROCESS_ARRIVAL, process.arrival_time, process, memory_manager)
        event_handler.add_event(event)

    event_handler.run_events()


if __name__ == "__main__":
    main()
