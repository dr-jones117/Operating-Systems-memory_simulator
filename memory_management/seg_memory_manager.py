from algorithm.algorithm import FitStrategy
from logger import Logger
from memory_management.memory_manager import MemoryManager
from process_system.process import Process


class SegMemoryManager(MemoryManager):
    def __init__(self, logger: Logger, fit_strategy: FitStrategy, mem_size: int):
        super().__init__(logger, mem_size)
        self.fit_strategy = fit_strategy

    def allocate_process(self) -> Process:
        if len(self.process_queue) <= 0:
            return None
        
        self.memory_map.sort(key=lambda x: x[0])
        
        for process in self.process_queue:
            skip_process = False
            copied_map = self.memory_map.copy()
            
            for idx, segment in enumerate(process.memory_segments):
                if skip_process:
                    continue

                idx_map, start_addr, end_addr  = self.fit_strategy.get_position(copied_map, segment)
                
                if idx_map != -1:
                    copied_map.insert(idx_map, (start_addr, start_addr + segment, f"Process {process.id}, Segment {idx}"))
                    if start_addr + segment < end_addr:
                        copied_map[idx_map + 1] = (start_addr + segment, end_addr, 'Hole')
                    else:
                        del copied_map[idx_map + 1]
                else:
                    skip_process = True
                    continue

            if skip_process:
                continue

            self.process_queue.remove(process)
            self.memory_map = copied_map     
            return process
                    
        return None

    
    def deallocate_process(self, process: Process):
        for i, (start, end, status) in enumerate(self.memory_map):
            if f"Process {process.id}" in status:
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

                self.deallocate_process(process)


        