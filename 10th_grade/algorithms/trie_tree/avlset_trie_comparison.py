from random import randint, choices
from string import ascii_lowercase as alphabet
from time import time
from typing import Callable
from secrets import token_urlsafe
import tracemalloc

from trie_tree import TrieNode
from avl_set import Set


N = 6

tracemalloc.start()


def resources_counter(func: Callable):
    def wrapper(*args, **kwargs):
        st_time = time()

        tracemalloc.reset_peak()
        st_mem, _ = tracemalloc.get_traced_memory()

        res = func(*args, **kwargs)

        mem_delt = tracemalloc.get_traced_memory()[1] - st_mem
        time_delt = round(time() - st_time, 5)

        print(
            f"Runtime of {func.__name__.upper()} is {time_delt}s. "
            f"Allocated memmory is {mem_delt} bytes"
        )
        return res
    return wrapper


def gen_prefix_test(size: int):
    def helper(size: int, lvl: int = 0):
        if size <= lvl:
            yield ''
        else:
            for char in choices(alphabet, k=3):
                suffixes = helper(size, lvl + 1)
                for suffix in suffixes:
                    yield char * randint(2, 4) + suffix

    return list(helper(size))


def gen_random_test(size: int):
    def helper(size: int, lvl: int = 0):
        if size <= lvl:
            yield ''
        else:
            for _ in range(3):
                suffixes = helper(size, lvl + 1)
                for suffix in suffixes:
                    yield token_urlsafe(randint(2, 4)) + suffix

    return list(helper(size))


if __name__ == "__main__":
    print("Testing for prefix string:")
    strings = gen_prefix_test(N)
    resources_counter(TrieNode)(strings)
    resources_counter(Set)(strings)

    print("\n", "--" * 15, end="\n\n")

    print("Testing for random string:")
    strings = gen_random_test(N)
    resources_counter(TrieNode)(strings)
    resources_counter(Set)(strings)
