from typing import Any, Optional
from time import time as now


def List(type):
    class ListWrapper(type):
        spent_memory: int = 0
        amount_get_requests: int = 0
        amount_set_requests: int = 0

        def __init__(self, lst) -> None:
            super().__init__(lst)
            self.spent_memory = len(lst) * 4

        def append(self, __object) -> None:
            super().append(__object)
            self.spent_memory += 4

        def __getitem__(self, index) -> Any:
            self.amount_get_requests += 1
            return super().__getitem__(index)

        def __setitem__(self, index: int, value) -> None:
            super().__setitem__(index, value)
            self.amount_set_requests += 1

        def __add__(self, other):
            new_list = List(list)(super().__add__(other))
            new_list.amount_get_requests = self.amount_get_requests + other.amount_get_requests
            new_list.amount_set_requests = self.amount_set_requests + other.amount_set_requests
            new_list.spent_memory = self.spent_memory + other.spent_memory
            return new_list

    return ListWrapper

def resousrs_checker(funk):

    def wrapper(lst: List) -> dict:
        start_time = now()
        result_function = funk(lst)
        finish_time = now()
        spent_memory = result_function.spent_memory
        if result_function is lst:
            spent_memory = 0
        spent_time = finish_time - start_time

        return {"time": spent_time,
                "result": result_function,
                "memory": spent_memory,
                "get_requests": lst.amount_get_requests + result_function.amount_get_requests,
                "set_requests": lst.amount_set_requests + result_function.amount_set_requests}
    return wrapper
