class Stack:
    __value: list

    def __init__(self, arg=None) -> None:
        if isinstance(arg, list):
            self.__value = arg
        elif isinstance(arg, int):
            self.__value = [arg]
        elif not arg:
            self.__value = []
        else:
            raise TypeError(f"Unknown type argument: {type(arg)}")

    def pop(self):
        self.__value.pop(-1)

    def push(self, value):
        self.__value.append(value)

    def top(self):
        return self.__value[-1]

    def size(self):
        return len(self.__value)

    def __str__(self) -> str:
        return ' '.join(self.__value)
