from __future__ import annotations

from typing import Generator, Iterable
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

    def __init__(self, collection: Iterable[str] = []) -> None:
        self.nodes = Dict[str, TrieNode]()
        for string in collection:
            self.add(string)

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

        new_node.nodes[suffix] = self.nodes[full_key]

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

    def __contains__(self, string: str) -> bool:
        if len(string) == 0:
            return END_CHAR in self.nodes

        for key, subtrie in self.nodes.to_list():
            if string.startswith(key):
                return string[len(key):] in subtrie

        return False

    def _get_strings(self) -> Generator[str, None, None]:
        nodes = self.nodes.to_list()
        for char, subtrie in nodes:
            if char == END_CHAR:
                yield ""
            else:
                for substr in subtrie._get_strings():
                    yield char + substr

    def __iter__(self):
        return self._get_strings()

    def __str__(self):
        strings = self._get_strings()
        return '\n'.join(strings)
