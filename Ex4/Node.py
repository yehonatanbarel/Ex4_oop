class Node(object):
    _key: int
    _dist: float
    _visited: bool
    _pos: tuple

    def __init__(self, key: int, pos: tuple = None):
        self._pos = pos
        self._key = key
        self._dist = float('inf')
        self._visited = False

    def get_key(self) -> int:
        return self._key

    def get_dist(self) -> float:
        return self._dist

    def set_dist(self, dist: float) -> None:
        self._dist = dist

    def get_visited(self) -> float:
        return self._visited

    def set_visited(self, visited: bool) -> None:
        self._visited = visited


    def get_pos(self) -> tuple:
        return self._pos

    def set_pos(self, pos: tuple) -> None:
        self._pos = pos

    def get_x(self) -> float:
        return self._pos[0]

    def get_y(self) -> float:
        return self._pos[1]

    def get_pos_str(self) -> str:
        return f'{self._pos[0]},{self._pos[1]},{self._pos[2]}'

    def __repr__(self):
        return f'id: {self._key}, pos: {self._pos}'

    def __eq__(self, other):
        return (self._key == other._key) and (self.g == other.g)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self._key < other._key) and (self.g < other.g)

    def __gt__(self, other):
        return (self._key > other._key) and (self.g > other.g)

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)