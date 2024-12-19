from random import randint
from typing import Generator
from secrets import token_urlsafe as gen_string


AMOUNT_TESTS = 5


def gen_random_set_elements(size: int) -> list[str]:
    return [
        gen_string(randint(5 * size, 10 * size))
        for _ in range(randint(5**(size+1), size * 5**(size+1)))
    ]


def gen_set_tests() -> Generator[list[str], None, None]:
    for lvl in range(1, AMOUNT_TESTS):
        yield gen_random_set_elements(lvl)
