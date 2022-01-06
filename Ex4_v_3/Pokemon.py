class Pokemon:
    _value: float
    _type: int
    _pos: tuple
    _id: int


    def __init__(self, value: float,type:int, pos: tuple,id: int):
        self._value = value
        self._type = type
        self._pos = pos
        self._id = id



    def get_value(self) -> float:
        return self._value

    def set_value(self, value: float) -> None:
        self._value = value

    def get_type(self) -> int:
        return self._type

    def set_type(self, type: int) -> None:
        self._type = type

    def get_pos(self) -> tuple:
        return self._pos

    def set_pos(self, pos: tuple) -> None:
        self._pos = pos


    def get_id(self) -> int:
        return self._id

    def set_id(self, id: int) -> None:
        self._id = id

    def __repr__(self):
        return f"{self._id}: vlaue: {self.get_value()}, type: {self._type}, pos: {self._pos}, id: {self._id}"
