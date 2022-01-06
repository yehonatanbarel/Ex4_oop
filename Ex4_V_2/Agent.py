from Node import Node


class Agent(object):
    _id: int
    _value: float
    _src: int
    _dest: int
    _speed: float
    _pos: tuple

    def __init__(self, id: int, value: float, src: int, dest: int, speed: float, pos: tuple):
        self._id = id
        self._value = value
        self._src = src
        self._dest = dest
        self._speed = speed
        self._pos = pos

    def get_id(self) -> int:
        return self._id

    def set_id(self, id: int) -> None:
        self._id = id

    def get_value(self) -> float:
        return self._value

    def set_value(self, value: float) -> None:
        self._value = value

    def get_src(self) -> int:
        return self._src

    def set_src(self, src: int) -> None:
        self._src = src

    def get_dest(self) -> int:
        return self._dest

    def set_dest(self, dest: int) -> None:
        self._dest = dest

    def get_speed(self) -> float:
        return self._speed

    def set_speed(self, speed: float) -> None:
        self._speed = speed

    def get_pos(self) -> tuple:
        return self._pos

    def set_pos(self, pos: tuple) -> None:
        self._pos = pos

    def __repr__(self):
        return f"id: {self._id}, value: {self._value}, src: {self._src}, dest: {self._dest}, speed: {self._speed}, pos: {self._pos}"
