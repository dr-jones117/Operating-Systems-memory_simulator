from typing import List
from logger import Logger


class FitStrategy:
    def __init__(self, logger: Logger):
        self.logger = logger

    def get_position(self, map: List, size: int) -> int:
        pass


class FirstStrategy(FitStrategy):
    def __init__(self, logger: Logger):
        super().__init__(logger)

    def get_position(self, map: List, size: int) -> int:
        for i, (start, end, status) in enumerate(map):
            if status == 'Hole' and (end - start) >= size:
                return i, start, end
            
        return -1, -1, -1


class BestStrategy(FitStrategy):
    def __init__(self, logger: Logger):
        super().__init__(logger)

    def get_position(self, map: List, size: int) -> int:
        self.logger.log('Best fitting')


class WorstStrategy(FitStrategy):
    def __init__(self, logger: Logger):
        super().__init__(logger)

    def get_position(self, map: List, size: int) -> int:
        self.logger.log("worst fitting!")

