# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Common Prefix Search with Double Array."""

# Not found means label
NOT_FOUND = -1


class DoubleArray(object):
    """Common Prefix Search with Double Array."""
    def __init__(self):
        self._base = [0]
        self._check = []
        self._index2char = [""]
        self._char2index = {}
        self._index2word = {}
        self._word2index = {}

    def craete(self, words):
        for w in words:
            parent = 0
            for i, c in enumerate(w):
                print(parent)
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
                    print(child, char_index)
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
