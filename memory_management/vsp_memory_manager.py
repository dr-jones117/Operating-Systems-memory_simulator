from algorithm.fit_strategy import FitStrategy
from memory_management.memory_manager import MemoryManager
from process_system.process import Process


class VspMemoryManager(MemoryManager):
    def __init__(self, fit_strategy: FitStrategy, mem_size: int):
        super().__init__(mem_size)
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
                    start, _, _ = self.memory_map[i - 1]
                    self.memory_map[i] = (start, end, 'Hole')
                    del self.memory_map[i - 1]
                    i -= 1
                
                if i < len(self.memory_map) - 1 and self.memory_map[i + 1][2] == 'Hole':
                    _, next_end, _ = self.memory_map[i + 1]
                    self.memory_map[i] = (start, next_end, 'Hole')
                    del self.memory_map[i + 1]
                return