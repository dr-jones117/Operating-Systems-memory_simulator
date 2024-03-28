from typing import List


class Process:
    def __init__(self, id: int, arrival_time: int, memory_lifetime: int, memory_segments: List[int]):
        self.id: int = id
        self.arrival_time = arrival_time
        self.memory_lifetime: int = memory_lifetime
        self.memory_segments: List[int] = memory_segments

    def total_memory_amount(self) -> int:
        return sum(self.memory_segments)
    
    def __str__(self):
        return f"id: {self.id}, arr: {self.arrival_time}, lifetime: {self.memory_lifetime}, total_memory: {self.total_memory_amount()}, mem_segments: {self.memory_segments}"
