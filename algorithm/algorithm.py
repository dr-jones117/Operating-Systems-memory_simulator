from typing import List
from logger import Logger


class FitStrategy:
    def __init__(self, logger: Logger):
        self.logger = logger

    def do_allocation(self, map: List):
        pass


class FirstStrategy(FitStrategy):
    def __init__(self, logger: Logger):
        super().__init__(logger)

    def do_allocation(self, map: List):
        self.logger.log('First fitting!')


class BestStrategy(FitStrategy):
    def __init__(self, logger: Logger):
        super().__init__(logger)

    def do_allocation(self, map: List):
        self.logger.log('Best fitting')


class WorstStrategy(FitStrategy):
    def __init__(self, logger: Logger):
        super().__init__(logger)

    def do_allocation(self, map: List):
        self.logger.log("worst fitting!")

