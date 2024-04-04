from typing import List


class FitStrategy:
    def get_position(self, map: List, size: int) -> int:
        pass


class FirstStrategy(FitStrategy):
    def get_position(self, map: List, size: int) -> int:
        for i, (start, end, status) in enumerate(map):
            if status == 'Hole' and (end - start) >= size:
                return i, start, end
            
        return -1, -1, -1
    

class PageStrategy(FitStrategy):
    def get_position(self, map: List, size: int) -> int:
        for i, (start, end, status) in enumerate(map):
            if status == 'Free Frame(s)' and (end - start) >= size:
                return i, start, end
            
        return -1, -1, -1


class BestStrategy(FitStrategy):
    def get_position(self, map: List, size: int) -> int:
        possible_holes = []

        for i, (start, end, status) in enumerate(map):
            if status == 'Hole' and (end - start) >= size:
                possible_holes.append((i, (int(start), int(end), status)))

        if len(possible_holes) <= 0:
            return -1, -1, -1
        
        sorted_possible_holes = sorted(possible_holes, key=lambda x: x[1][1] - x[1][0])
        idx, (start, end, status) = sorted_possible_holes[0]
        return idx, start, end


class WorstStrategy(FitStrategy):
    def get_position(self, map: List, size: int) -> int:
        possible_holes = []

        for i, (start, end, status) in enumerate(map):
            if status == 'Hole' and (end - start) >= size:
                possible_holes.append((i, (int(start), int(end), status)))

        if len(possible_holes) <= 0:
            return -1, -1, -1
        
        sorted_possible_holes = sorted(possible_holes, key=lambda x: x[1][1] - x[1][0])
        idx, (start, end, status) = sorted_possible_holes[len(sorted_possible_holes) - 1]
        return idx, start, end

