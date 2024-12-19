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
    nodes: Dict[str, TrieNode | None]

    def __init__(self) -> None:
        self.nodes = Dict[str, TrieNode]()

    def add(self, string: str) -> None:
        if len(string) == 0:
            self.nodes[END_CHAR] = None

        nodes = self.nodes.to_list()
        if len(nodes) == 0:
            self.nodes[string] = TrieNode()
            self.nodes[string].nodes[END_CHAR] = None
            return

        for key, subtrie in nodes:
            if string.startswith(key):
                subtrie.add(string[len(key):])
                return

        longest_common_prefix = ""
        full_key = ""
        for key, subtrie in nodes:
            cur_common_prefix = get_common_prefix(key, string)
            if len(cur_common_prefix) > len(longest_common_prefix):
                longest_common_prefix = cur_common_prefix
                full_key = key

        if len(longest_common_prefix) == 0:
            self.nodes[string] = TrieNode()
            self.nodes[string].nodes[END_CHAR] = None
            return

        new_node = self.nodes[longest_common_prefix] = TrieNode()

        suffix = full_key[len(longest_common_prefix):]
        remaining_string = string[len(longest_common_prefix):]

        new_node.nodes[suffix] = deepcopy(self.nodes[full_key])

        new_node.add(remaining_string)

        self.nodes.delete(full_key)

    def remove(self, string: str) -> None:
        if len(string) == 0:
            if END_CHAR in self.nodes:
                self.nodes.delete(END_CHAR)
                return
            else:
                raise "No such string"

        nodes = self.nodes.to_list()
        for key, subtrie in nodes:
            if string.startswith(key):
                suffix = string[len(key):]
                subtrie.remove(suffix)
                return

        raise "No such string"

    def _get_longest_common_prefix(self) -> tuple[str, TrieNode]:
        nodes = self.nodes.to_list()
        if len(nodes) == 1 and nodes[0][0] != END_CHAR:
            longest_prefix, node = nodes[0][1]._get_longest_common_prefix()
            return nodes[0][0] + longest_prefix, node
        else:
            return "", self

    def __contains__(self, string: str) -> bool:
        if len(string) == 0:
            return END_CHAR in self.nodes

        cur_char = string[0]
        return\
            False if self.nodes[cur_char] is None\
            else string[1:] in self.nodes[cur_char]

    def _get_strings(self) -> Generator[str, None, None]:
        nodes = self.nodes.to_list()
        for char, subtrie in nodes:
            if char == END_CHAR:
                yield ""
            else:
                for substr in subtrie._get_strings():
                    yield char + substr

    def __str__(self):
        strings = self._get_strings()
        return '\n'.join(strings)


t = TrieNode()
t.add("aaa")
t.add("aaab")
t.add("aaac")
t.add("aaae")
t.add("aabb")
t.remove("aaa")
t.remove("aabb")
print(t)
