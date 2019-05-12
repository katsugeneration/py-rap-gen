# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Common Prefix Search with Double Array."""
import copy


# Not found label
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


class DoubleArray(TrieBase):
    """Common Prefix Search with Double Array."""
    def __init__(self, words):
        self._index2char = [""]
        self._char2index = {}
        self._index2word = {}
        self._word2index = {}
        self._base, self._check = self.create(words)

    def create(self, words):
        """Create double array.

        double array consists two arrays. base and check
        base is transition node array.
        check is parent node check array.
        both arrays are node length

        Args:
            words (List[String]): target yomi foramt words list.

        Return:
            base (List[Int]): transition node array.
            check (List[Int]): parent node check array.
        """
        table = super().create(words)
        index2word = copy.deepcopy(self._index2word)
        self._index2word = {}
        self._word2index = {}
        base = [0]
        check = [NOT_FOUND]

        def _search(p, n):
            """Deep First Searh for creating double array.

            Args:
                p (Int): transition table parent node index.
                n (Int): double array parent node index.
            """
            if p in index2word:
                # Update word node index to double array index
                w = index2word[p]
                self._index2word[n] = w
                self._word2index[w] = n

            if p >= len(table):
                return

            if n >= len(base):
                base.extend([NOT_FOUND] * (n - len(base) + 1))

            children = [(char_index, c) for char_index, c in enumerate(table[p]) if c != NOT_FOUND]

            if len(children) == 0:
                # Case n is end node
                return

            # Search indexies meeting all conditons
            min_char_index = min(children, key=lambda x: x[0])[0]
            max_char_index = max(children, key=lambda x: x[0])[0]
            start_index = min_char_index

            is_end = False
            while not is_end:
                try:
                    min_index = check.index(NOT_FOUND, start_index)
                except ValueError:
                    check.append(NOT_FOUND)
                    min_index = len(check) - 1
                base[n] = min_index - min_char_index

                if (base[n] + max_char_index) >= len(check):
                    check.extend([NOT_FOUND] * (base[n] + max_char_index - len(check) + 1))

                is_end = all([check[base[n] + char_index] == NOT_FOUND for char_index, _ in children])
                start_index = min_index + 1

            # Set searched information
            for char_index, _ in children:
                check[base[n] + char_index] = n
            for char_index, c in children:
                _search(c, base[n] + char_index)

        _search(0, 0)
        return base, check
