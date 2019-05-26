# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
"""Graph Shortes Path Solution."""
import sys


class Node(object):
    """Graph Node Object."""
    def __init__(self, start_pos, word):
        self.start_pos = start_pos
        self.word = word
        self.cost = 0
        self.prev = None

    def __eq__(self, other):
        return (
            self.start_pos == other.start_pos and
            self.word == other.word and
            self.cost == other.cost and
            self.prev == other.prev
        )

    def __hash__(self):
        return hash((
            self.start_pos,
            self.word,
            self.cost,
            self.prev))


class Graph(object):
    """Graph Object."""
    def __init__(self):
        self.nodes = []  # common endo position words list
        self.BOS = Node(0, "")
        self.EOS = Node(-1, "")

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
        g.nodes[0] = [g.BOS]
        g.EOS = Node(len(tone), "")
        g.nodes[len(tone) + 1] = [g.EOS]

        for i in range(len(tone)):
            for s in prefix_searcher.prefix_search(tone[i:]):
                g.nodes[i + len(s)].extend([Node(i, w) for w in tone_list[s]])

        return g

    def get_node_cost(self, node):
        """Return node cost.

        Args:
            node (Node): target node object.

        Return:
            cost (Int): node cost value.
        """
        # TODO: return predifiend cost.
        return 0

    def get_edge_cost(self, prev, node):
        """Return prev to node edge cost.

        Args:
            prev (Node): previous node object.
            node (Node): target node object.

        Return:
            cost (Int): edge cost value.
        """
        # TODO: return predifiend cost.
        return 0

    def search_shortest_path(self):
        """Return graph shortest path.

        Return:
            path (List[Node]): node list constructs shortest path.
        """
        N = len(self.nodes)

        # cost calculation (viterbi algorithm)
        for i in range(1, N):
            for node in self.nodes[i]:
                node.cost = sys.maxsize
                node_cost = self.get_node_cost(node)
                for prev in self.nodes[node.start_pos]:
                    edge_cost = self.get_edge_cost(prev, node)
                    cost = prev.cost + edge_cost + node_cost
                    if cost < node.cost:
                        node.cost = cost
                        node.prev = prev

        # search shortest path
        node = self.EOS
        result = []
        while node != self.BOS:
            result.insert(0, node)
            node = node.prev

        return result
