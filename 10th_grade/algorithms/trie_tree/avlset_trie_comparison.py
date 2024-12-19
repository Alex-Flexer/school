from random import randint, choices
from string import ascii_lowercase as alphabet
from time import time
from typing import Callable
from secrets import token_urlsafe

from trie_tree import TrieNode
from avl_set import Set


N = 7


def time_counter(func: Callable):
    def wrapper(*args, **kwargs):
        st_time = time()
        res = func(*args, **kwargs)
        time_delt = round(time() - st_time, 5)
        print(f"Runtime of {func.__name__.upper()} is {time_delt}s")
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
    time_counter(TrieNode)(strings)
    time_counter(Set)(strings)

    print("\n", "--" * 15, end="\n\n")

    print("Testing for random string:")
    strings = gen_random_test(N)
    time_counter(TrieNode)(strings)
    time_counter(Set)(strings)
