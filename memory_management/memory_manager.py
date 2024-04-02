from logger import Logger

class MemoryManager:
    def __init__(self, logger: Logger, mem_size: int, page_size: int = None):
        self.logger = logger;
        self.mem_size = mem_size
        self.page_size = page_size
        self.memory_map = [(0, self.mem_size, 'Hole')]
        