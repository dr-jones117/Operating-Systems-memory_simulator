from algorithm.algorithm import PageStrategy
from logger import Logger
from memory_management.memory_manager import MemoryManager
from process_system.process import Process


class PagMemoryManager(MemoryManager):
    def __init__(self, logger: Logger, mem_size: int, page_size: int):
        super().__init__(logger, mem_size)
        self.page_size = page_size
        self.fit_strategy = PageStrategy(logger)
        self.memory_map = [(0, self.mem_size, 'Free Frame(s)')]

    def allocate_process(self) -> Process:
        if len(self.process_queue) <= 0:
            return None
        
        self.memory_map.sort(key=lambda x: x[0])
        
        for process in self.process_queue:
            skip_process = False
            copied_map = self.memory_map.copy()

            pages = [self.page_size for _ in range(process.total_memory_amount() // self.page_size)]
            if process.total_memory_amount() % self.page_size != 0:
                pages.append(self.page_size)

            for idx, page in enumerate(pages):
                if skip_process:
                    continue

                idx_map, start_addr, end_addr  = self.fit_strategy.get_position(copied_map, page)
                
                if idx_map != -1:
                    copied_map.insert(idx_map, (start_addr, start_addr + page, f"Process {process.id}, Page {idx + 1}"))
                    if start_addr + page < end_addr:
                        copied_map[idx_map + 1] = (start_addr + page, end_addr, 'Free Frame(s)')
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
                self.memory_map[i] = (start, end, 'Free Frame(s)')

                if i > 0 and self.memory_map[i - 1][2] == 'Free Frame(s)':
                    start, _, _ = self.memory_map[i - 1]
                    self.memory_map[i] = (start, end, 'Free Frame(s)')
                    del self.memory_map[i - 1]
                    i -= 1
                
                if i < len(self.memory_map) - 1 and self.memory_map[i + 1][2] == 'Free Frame(s)':
                    _, next_end, _ = self.memory_map[i + 1]
                    self.memory_map[i] = (start, next_end, 'Free Frame(s)')
                    del self.memory_map[i + 1]

                self.deallocate_process(process)