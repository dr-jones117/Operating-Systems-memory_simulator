class MemoryManager:
    def __init__(self, mem_size: int, page_size: int = None):
        self.mem_size = mem_size
        self.page_size = page_size
        self.memory_map = {}