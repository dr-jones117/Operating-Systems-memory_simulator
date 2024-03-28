from typing import List
from process_system.process import Process

class ProcessFile:
    def __init__(self, path: str):
        self.path: int = path;

    def get_processes(self) -> List[Process]:
        try:
            file = open(self.path, 'rt')
            processes: List[Process] = []
            num_processes = int(file.readline())

            for _ in range(num_processes):
                id: int = int(file.readline())
                time_info = file.readline().split()

                arrival_time = int(time_info[0])
                mem_lifetime = int(time_info[1])

                memory_info = file.readline().split()
                memory_segments = [int(seg) for seg in memory_info[1:]]

                file.readline()

                process = Process(id, arrival_time, mem_lifetime, memory_segments)
                processes.append(process)

            return processes
             
        except FileNotFoundError:
            print("Error: File not found:", self.path)
            exit(1)