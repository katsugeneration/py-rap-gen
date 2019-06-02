# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Counter object."""


class LossyCounter(object):
    """Count using Lossy Counting algorithme."""
    def __init__(self, epsilon=1e-5):
        """Initialize counter object.
        Args:
            epsilon: Lossy Counting algorithme quality parameter
        """
        self._symbol_num = 0
        self._buckets_num = 0
        self.epsilon = epsilon
        self._items = {}
        self.vocab = []

    def count(self, data):
        """Count data element nums.

        Args:
            data (List[X]): data object list.
        """
        self._symbol_num = 0
        self._buckets_num = 0

        for symbol in data:
            self._symbol_num += 1

            if symbol in self._items:
                self._items[symbol] += 1
            else:
                self._items[symbol] = self._buckets_num + 1

            if self._symbol_num % int(1 / self.epsilon) == 0:
                self._buckets_num += 1
                self._items = self._remove_items(self._items, self._buckets_num)

    def _remove_items(self, items, threshold):
        """Remove elements lower count than threshold.

        Args:
            items (Hash[X, Int]): data object count list.
            threshold (Int): minimum count.
        Return:
            ret (Hash[X]): updated data object count list
        """
        ret = dict(filter(lambda x: x[1] >= threshold, items.items()))
        return ret
