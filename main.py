from typing import List
from algorithm.algorithm import BestStrategy, FirstStrategy, WorstStrategy
from event_system.event import Event
from logger import Logger
from event_system.event_type import *
from process_system.process import Process
from process_system.process_file import ProcessFile
from memory_management.memory_manager import PagMemoryManager, SegMemoryManager, VspMemoryManager
from memory_management.memory_policy import MemoryPolicy
from event_system.event_handler import EventHandler
from algorithm.algorithm_type import AlgorithmType


def main():
    # Get initial parameters from user
    mem_size: int = int(input('Memory Size: ') )# represented in kBs
    policy: int = int(input('Memory management policy (1 - VSP, 2 - PAG, 3 - SEG): '))
    page_size: int = 0
    algorithm: int = 0
    
    # If we are paging, we don't need to run a fitting algorithm, instead, we need the page size
    if policy == MemoryPolicy.PAG.value:
        page_size = int(input('Page/Frame Size: '))
    else:
        algorithm = int(input('Fit algorithm (1 - first-fit, 2 - best-fit, 3 - worst-fit): '))

    path: str = input('Process Information File Name: ')
    out_path: str = input('Output File Name: ')

    # Get the processes from the path provided by the user
    process_file: ProcessFile = ProcessFile(path)
    processes: List[Process] = process_file.get_processes()

    logger = Logger(out_path)

    # Create the fitting strategy if needed
    if algorithm == AlgorithmType.FIRST.value:
        algorithm = FirstStrategy(logger)
    elif algorithm == AlgorithmType.BEST.value:
        algorithm == BestStrategy(logger)
    elif algorithm == AlgorithmType.WORST.value:
        algorithm == WorstStrategy(logger)

    # Create the correct memory manager type
    memory_manager = None
    if policy == MemoryPolicy.VSP.value:
        memory_manager = VspMemoryManager(logger, algorithm, mem_size)
    elif policy == MemoryPolicy.SEG.value:
        memory_manager = SegMemoryManager(logger, algorithm, mem_size)
    elif policy == MemoryPolicy.PAG.value:
        memory_manager = PagMemoryManager(logger, algorithm, mem_size, page_size)
    else:
        print(f"Error: Invalid policy ({policy})")
        exit(1)

    # Create the event handler based on the memory manager
    event_handler = EventHandler(logger, memory_manager)

    # Each process will need an arrival event, add them to the event handler
    for process in processes:
        event = Event(EventType.PROCESS_ARRIVAL, process.arrival_time, process)
        event_handler.add_event(event)

    # Finally, run all of the events
    event_handler.run_events()


if __name__ == "__main__":
    main()
