class Pokemon:
    _id: int
    _value: float
    _pos: tuple

    def __init__(self, id: int, value: float, pos: tuple):
        self._id = id
        self._value = value
        self._pos = pos

    def get_id(self) -> int:
        return self._id

    def set_id(self, id: int) -> None:
        self._id = id

    def get_value(self) -> float:
        return self._value

    def set_value(self, value: float) -> None:
        self._value = value

    def get_pos(self) -> tuple:
        return self._pos

    def set_pos(self, pos: tuple) -> None:
        self._pos = pos

    def __repr__(self):
        return f"id = {self._id}, value = {self._value}, pos = {self._pos}"
