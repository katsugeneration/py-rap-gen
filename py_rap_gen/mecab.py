# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.

import MeCab

tagger = MeCab.Tagger("")


class Word(object):
    """Word class from mecab output."""

    def __init__(self, output):
        """Initialize mecab one word class from mecab one line."""
        pos, pos1, surface, base, yomi = self._parse_mecab_output(output)
        self.pos = pos
        self.pos1 = pos1
        self.surface = surface
        self.base = base
        self.yomi = yomi

    @classmethod
    def _parse_mecab_output(cls, output):
        """Return mecab one word parsing results.

        Args:
            output (str): mecab one line.
        Return:
            pos (str): most import part-of-speech tag.
            pos1 (str): second import part-of-speech tag.
            surface (str): word surface format string.
            base (str): word base format string.
            yomi (str): word surface yomi string.
        """
        surface = output.split("\t")[0].strip()
        parts = output.split("\t")[1].strip().split(",")
        pos = parts[0]
        pos1 = parts[1]
        base = parts[6] if '*' != parts[6] else surface
        yomi = parts[7] if len(parts) >= 8 else surface
        return pos, pos1, surface, base, yomi


class Sentence(object):
    """Sentence class from mecab output."""

    def __init__(self, output):
        """Initialize mecab one Sentence class from mecab one line."""
        self.words = self._parse_mecab_output(output)

    @classmethod
    def _parse_mecab_output(cls, output):
        """Return mecab sentence parsing results.

        Args:
            output (str): mecab outputs.
        Return:
            words (List[Word]): parsing output word class array.
        """
        words = [Word(line) for line in output.strip().split('\n') if line != 'EOS']
        return words


def parse(s):
    """Parsing mecab.

    Args:
        s (str): target string.
    Return:
        sentence (Sentence): parsed sentence object.
    """
    return Sentence(tagger.parse(s))
