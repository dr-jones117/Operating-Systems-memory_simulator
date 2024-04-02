from algorithm.algorithm import FitStrategy
from logger import Logger
from process_system.process import Process

class MemoryManager:
    def __init__(self, logger: Logger, mem_size: int):
        self.logger = logger;
        self.mem_size = mem_size
        self.memory_map = [(0, self.mem_size, 'Hole')]
        self.process_queue = []
        self.turnaround_time = 0

    def process_queue_str(self):
        return [process.id for process in self.process_queue]
    
    def add_process(self, process: Process):
        self.process_queue.append(process)
    
    def get_memory_map_str(self) -> str:
        map_str = "Memory Map: "

        for start, end, status in self.memory_map:
            map_str += f"{start}-{end - 1}: {status}\n\t\t"   

        map_str = map_str[0:-1]
        return map_str

    def allocate_process(self) -> bool:
        pass
        
    def deallocate_process(self, process: Process):
        pass

class VspMemoryManager(MemoryManager):
    def __init__(self, logger: Logger, fit_strategy: FitStrategy, mem_size: int):
        super().__init__(logger, mem_size)
        self.fit_strategy = fit_strategy

    def allocate_process(self) -> Process:
        if len(self.process_queue) <= 0:
            return None
        
        self.memory_map.sort(key=lambda x: x[0])
        
        for process in self.process_queue:
            idx, start_addr, end_addr  = self.fit_strategy.get_position(self.memory_map, process.total_memory_amount())
            if idx != -1:
                self.memory_map.insert(idx, (start_addr, start_addr + process.total_memory_amount(), f"Process {process.id}"))
                if start_addr + process.total_memory_amount() < end_addr:
                    self.memory_map[idx + 1] = (start_addr + process.total_memory_amount(), end_addr, 'Hole')
                else:
                    del self.memory_map[idx + 1]
                self.process_queue.remove(process)
                    
                return process
                    
        return None

    
    def deallocate_process(self, process: Process):
        for i, (start, end, status) in enumerate(self.memory_map):
            if status == f"Process {process.id}":
                self.memory_map[i] = (start, end, 'Hole')

                if i > 0 and self.memory_map[i - 1][2] == 'Hole':
                    prev_start, _, _ = self.memory_map[i - 1]
                    self.memory_map[i] = (prev_start, end, 'Hole')
                    del self.memory_map[i - 1]
                    i -= 1
                
                if i < len(self.memory_map) - 1 and self.memory_map[i + 1][2] == 'Hole':
                    _, next_end, _ = self.memory_map[i + 1]
                    self.memory_map[i] = (start, next_end, 'Hole')
                    del self.memory_map[i + 1]
                return


class SegMemoryManager(MemoryManager):
    def __init__(self, logger: Logger, fit_strategy: FitStrategy, mem_size: int):
        super().__init__(logger, mem_size)
        self.fit_strategy = fit_strategy


class PagMemoryManager(MemoryManager):
    def __init__(self, logger: Logger, mem_size: int, page_size: int):
        super().__init__(logger, mem_size)
        self.page_size = page_size