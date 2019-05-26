# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Graph Shortes Path Solution."""


class Node(object):
    """Graph Node Object."""
    def __init__(self, start_pos, word):
        self.start_pos = start_pos
        self.word = word
        self.score = 0
        self.prev = None

    def __eq__(self, other):
        return (
            self.start_pos == other.start_pos and
            self.word == other.word and
            self.score == other.score and
            self.prev == other.prev
        )

    def __hash__(self):
        return hash((
            self.start_pos,
            self.word,
            self.score,
            self.prev))


BOS = Node(0, "")
EOS = Node(-1, "")


class Graph(object):
    """Graph Object."""
    def __init__(self):
        self.nodes = []  # common endo position words list

    @classmethod
    def construct_graph(cls, prefix_searcher, tone_list, tone):
        """Construct convert graph.

        Args:
            prefix_searcher (TrieBase): trie data
            tone_list (Hash[String, List[String]]): tone to tone dictionary.
            tone (String): target tone.

        Return:
            graph (Graph): new graph object.
        """
        g = Graph()

        for _ in range(len(tone) + 2):
            g.nodes.append([])
        g.nodes[0] = [BOS]
        g.nodes[len(tone) + 1] = [EOS]

        for i in range(len(tone)):
            for s in prefix_searcher.prefix_search(tone[i:]):
                g.nodes[i + len(s)].extend([Node(i, w) for w in tone_list[s]])

        return g
