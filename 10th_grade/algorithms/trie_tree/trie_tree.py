from __future__ import annotations

from typing import Callable, Any, Generator
from copy import deepcopy
import itertools

from avl_dict import Dict


def get_common_prefix(str1: str, str2: str) -> str:
    return ''.join(
        x[0]
        for x in itertools.takewhile(
            lambda x: x[0] == x[1],
            zip(str1, str2))
    )


END_CHAR = '\0'


class TrieNode:
    dict_: Dict[str, TrieNode | None]

    def __init__(self) -> None:
        self.dict_ = Dict[str, TrieNode]()
    
    def add(self, string: str) -> None:
       nodes = self.dict_.to_list()
       if len(nodes) == 0:
           self.dict_[string] = TrieNode()
           self.dict_[string].dict_[END_CHAR] = None
           return
       
       for key, subtrie in nodes:
           if string.startswith(key):
               subtrie.add(string[])
        
        
        
       # self.dict_[cur_char].add(string[1:])
    
    def remove(self, string: str) -> None:
        if len(string) == 0:
            self.dict_.delete(END_CHAR)
            return

        cur_char = string[0]
        if self.dict_[cur_char] is not None:
            self.dict_[cur_char].remove(string[1:])
            if len(self.dict_.to_list()) == 1:
                self.dict_.delete(cur_char)
    
    def _get_longest_common_prefix(self) -> tuple[str, TrieNode]:
        nodes = self.dict_.to_list()
        if len(nodes) == 1 and nodes[0][0] != END_CHAR:
            longest_prefix, node = nodes[0][1]._get_longest_common_prefix()
            return nodes[0][0] + longest_prefix, node
        else:
            return "", self

    def _optimize(self) -> None:
        longest_prefix, last_node = self._get_longest_common_prefix()
        if len(longest_prefix) >= 1:
                print("pref:", longest_prefix)
        self.dict_[longest_prefix] = last_node.dict_
        self.dict_ = last_node.dict_
        
    def optimize(self) -> None:
        self._optimize()
        for key, subtrie in self.dict_.to_list():
            if key != END_CHAR:
                subtrie.optimize()

    def __contains__(self, string: str) -> bool:
        if len(string) == 0:
            return END_CHAR in self.dict_

        cur_char = string[0]
        return\
            False if self.dict_[cur_char] is None\
            else string[1:] in self.dict_[cur_char]

    def _get_strings(self) -> Generator[str, None, None]:
        nodes = self.dict_.to_list()
        for char, subtrie in nodes:
            if char == END_CHAR:
                yield ""
            else:
                for substr in subtrie._get_strings():
                    yield self.prefix + char + substr

    def __str__(self):
        strings = self._get_strings()
        return '\n'.join(strings)

t = TrieNode()
# print(t.nodes.to_list())
t.add("abcd")
t.add("abce")
t.add("abk")
t.add("abkbbb1")
t.add("abkbbb2")
t.add("abkbbb3")
t.add("abkbbb")
t.add("abl")
t.add("abc")
t.optimize()
print(t)
# t.remove("abl")
# print("abl" in t)
# print(get_common_prefix("abcde", "abcd"))
