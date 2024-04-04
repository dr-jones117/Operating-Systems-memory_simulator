from typing import List
from algorithm.fit_strategy import FitStrategy
from process_system.process import Process

class MemoryManager:
    def __init__(self, mem_size: int):
        self.mem_size = mem_size
        self.memory_map = [(0, self.mem_size, 'Hole')]
        self.process_queue: List[Process] = []
        self.turnaround_time = 0

    def get_process_queue_str(self):
        id_list = [process.id for process in self.process_queue]
        return "[" + " ".join(map(str, id_list)) + "]"
    
    def add_process(self, process: Process):
        self.process_queue.append(process)
    
    def get_memory_map_str(self) -> str:
        map_str = "Memory Map: \n\t\t"

        for start, end, status in self.memory_map:
            map_str += f"{start}-{end - 1}: {status}\n\t\t"   

        map_str = map_str[0:-1]
        return map_str

    def allocate_process(self) -> Process:
        pass
        
    def deallocate_process(self, process: Process):
        pass

