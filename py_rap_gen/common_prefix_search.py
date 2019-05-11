# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Common Prefix Search with Double Array."""

# Not found means label
NOT_FOUND = -1


class TrieBase(object):
    """Common Prefix Search with Naive Transition Table."""
    def __init__(self, words):
        self._index2char = [""]
        self._char2index = {}
        self._index2word = {}
        self._word2index = {}
        self._table = self.create(words)

    def create(self, words):
        """Create trie transition table.

        trie transition table is shape (N, C)
        N is trie tree nose size.
        C is character vocabulary size.

        Args:
            words (List[String]): target yomi foramt words list.

        Return:
            table (List[List[Int]]): transition table.
        """
        table = [[]]

        for w in words:
            parent = 0
            for c in w:
                if c not in self._index2char:
                    self._index2char.append(c)
                    self._char2index[c] = len(self._index2char) - 1
                char_index = self._char2index[c]
                node = table[parent]

                if char_index >= len(node):
                    node.extend([NOT_FOUND] * (char_index - len(node) + 1))
                child = node[char_index]

                if child == NOT_FOUND:
                    table.append([])
                    child = len(table) - 1
                    node[char_index] = child
                parent = child

            if w not in self._index2word:
                self._index2word[parent] = w
                self._word2index[w] = parent

        return table

    def search(self, word):
        """Search common prefix words.

        Args:
            word (String): target prefix.

        Return:
            result (List[String]): matched words.
        """
        parent = 0
        for c in word:
            if c not in self._char2index:
                return []
            if self._char2index[c] >= len(self._table[parent]):
                return []

            parent = self._table[parent][self._char2index[c]]

            if parent == NOT_FOUND:
                return []
        return [self._index2word[i]
                for i in self.descendant(parent) + [parent]
                if i in self._index2word]

    def descendant(self, parent):
        """Return descendant node list.

        Args:
            parent (Int): target node index.

        Return:
            result (List[Int]): descendant node index list.
        """
        S = set()

        def _search(p):
            nonlocal S
            children = [c for c in self._table[p] if c != NOT_FOUND]
            S |= set(children)
            for c in children:
                _search(c)

        _search(parent)
        return list(S)


class DoubleArray(object):
    """Common Prefix Search with Double Array."""
    def __init__(self):
        self._base = [0]
        self._check = []
        self._index2char = [""]
        self._char2index = {}
        self._index2word = {}
        self._word2index = {}

    def create(self, words):
        for w in words:
            parent = 0
            for i, c in enumerate(w):
                if c not in self._index2char:
                    self._index2char.append(c)
                    self._char2index[c] = len(self._index2char) - 1
                char_index = self._char2index[c]

                if parent >= len(self._base):
                    self._base.extend([NOT_FOUND] * (parent - len(self._base) + 1))

                if self._base[parent] != NOT_FOUND:
                    # case parent has added to double array
                    child = self._base[parent] + char_index

                    if child >= len(self._check):
                        self._check.extend([NOT_FOUND] * (child - len(self._check) + 1))

                    if self._check[child] == NOT_FOUND:
                        # case parent has not added to double array
                        self._check[child] = parent
                        parent = child
                    elif self._check[child] == parent:
                        # case parent has added to double array
                        parent = child
                    else:
                        # case double array is conflict.
                        raise NotImplementedError()

                else:
                    try:
                        child = self._base.index(NOT_FOUND, char_index)
                    except ValueError:
                        if char_index < len(self._base):
                            self._base.append(NOT_FOUND)
                            child = len(self._check) - 1
                        else:
                            self._base.extend([NOT_FOUND] * (char_index - len(self._base) + 1))
                            child = self._base.index(NOT_FOUND, char_index)

                    self._base[parent] = child - char_index
                    if child >= len(self._check):
                        self._check.extend([NOT_FOUND] * (child - len(self._check) + 1))

                    if self._check[child] != NOT_FOUND and self._check[child] != parent:
                        # case double array is conflict.
                        raise NotImplementedError()
                    else:
                        self._check[child] = parent
                        parent = child

                if (i+1) == len(w):
                    if w not in self._index2word:
                        self._index2word[parent] = w
                        self._word2index[w] = parent
