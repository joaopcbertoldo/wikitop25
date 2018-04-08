from typing import List, Tuple
from numbers import Number


class RankItem:

    def __init__(self, content, score):
        self.content = content
        self.score = score

    def __eq__(self, other) -> bool:
        return self.score == other if isinstance(other, Number) else self.score == other.score

    def __ne__(self, other) -> bool:
        return self.score != other if isinstance(other, Number) else self.score != other.score

    def __gt__(self, other) -> bool:
        return self.score > other if isinstance(other, Number) else self.score > other.score

    def __ge__(self, other) -> bool:
        return self.score >= other if isinstance(other, Number) else self.score >= other.score

    def __lt__(self, other) -> bool:
        return self.score < other if isinstance(other, Number) else self.score < other.score

    def __le__(self, other) -> bool:
        return self.score <= other if isinstance(other, Number) else self.score <= other.score


class Rank:

    def __init__(self, size):
        self._size = size
        self._list: List[RankItem] = []

    def push(self, content, score):
        ri = RankItem(content, score)

        if not self._list:
            self._list.append(ri)
        else:
            list_len = len(self._list)
            max_size = self._size
            size = min(max_size, list_len)

            last_item = self._list[size - 1]
            if size == max_size and score <= last_item:
                return
            else:
                range_ = list(reversed(range(size)))
                for i in range_:
                    item = self._list[i]
                    # draw ??
                    if score <= item:
                        break
                if i == 0 and score > item:
                    i = -1

                i += 1
                new_item = RankItem(content, score)
                self._list.insert(i, new_item)

    def _clean(self):
        if len(self._list) > self._size:
            self._list = self._list[:self._size]

    @property
    def ranked_contents(self) -> List:
        self._clean()
        ret = [i.content for i in self._list]
        return ret

    @property
    def ranked_scores(self) -> List:
        self._clean()
        ret = [i.score for i in self._list]
        return ret

    @property
    def ranked_items(self) -> List[RankItem]:
        self._clean()
        ret = [i for i in self._list]
        return ret

    @property
    def ranked_tuples(self) -> List[Tuple]:
        self._clean()
        ret = [(i.content, i.score) for i in self._list]
        return ret
