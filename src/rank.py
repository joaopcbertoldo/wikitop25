from typing import List, Tuple, Callable, Union
from numbers import Number


class RankItem:

    def __init__(self, content, score):
        self._contents = [content]
        self.score = score

    def add_content(self, content):
        self._contents.append(content)

    @property
    def contents(self):
        return self._contents

    def __str__(self):
        contents_str = str(self._contents)
        contents_str =  contents_str if len(contents_str) < 50 else contents_str[:50] + '...'
        return f'RankItem(score: {self.score}, contents({len(self._contents)}): {contents_str})'

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


# ------------------------------------------------ RANK ----------------------------------------------------------------
class Rank:

    # init
    def __init__(self, name: str, maxlen: int, validate_fun: Callable):
        self._name = name
        self._maxlen = maxlen
        self._list: List[RankItem] = []
        self._validate_fun = validate_fun

    # len
    def __len__(self):
        return min(len(self._list), self._maxlen)

    # [] operator
    def __getitem__(self, index) -> RankItem:
        return self._list[index]

    # str
    def __str__(self):
        strs = ['\t' + str(ri) for ri in self.rank_items]
        strs.insert(0, f'Rank(name: {self._name}, len: {len(self)} (max: {self._maxlen}))')
        ret = '\n'.join(strs)
        return ret

    # first
    @property
    def first(self) -> Union[RankItem, None]:
        return self._list[0] if self._list else None

    # last
    @property
    def last(self) -> Union[RankItem, None]:
        return self._list[len(self) - 1] if self._list else None

    # has max len
    @property
    def has_max_len(self) -> bool:
        return len(self._list) >= self._maxlen

    # push
    def push(self, content, score):

        # if there is a validation function
        if self._validate_fun:

            # if it's not valid
            if not self._validate_fun(content):
                # return earlier
                return

        # in case the list is empty
        if not self._list:

            # create the item
            ri = RankItem(content, score)

            # append it to the list
            self._list.append(ri)

            # c'est fini
            return

        # the strategy is to compare bottom-up, because whenever the last in the rank is bigger than the pushed
        # content, there is no need to check the others (they are bigger too).

        # first item of the rank - if it got up to here, the list is not empty, so last returns something
        first_item = self.first

        # first check for the trivial case where the pushed is bigger than the first
        if score > first_item:

            # create the item
            ri = RankItem(content, score)

            # insert it in the first place
            self._list.insert(0, ri)

            # ret
            return

        # last item of the rank - if it got up to here, the list is not empty, so last returns something
        last_item = self.last

        # check for the case where it is smaller than the last item
        if score < last_item:

            # in the case it has already the maxlen, there is no need to consider it
            if self.has_max_len:
                return

            # otherwise it can just be added in the end
            else:
                # create the item
                ri = RankItem(content, score)

                # insert it in the first place
                self._list.append(ri)

                # get off
                return

        # decreasing range of indices of the rank
        indices = list(reversed(range(len(self))))

        # iterate decreasingly
        for i in indices:

            # get the item
            item = self[i]

            # in case that pushed has the same score
            if score == item:

                # add the content to that rank item
                self[i].add_content(content)

                # c'est fini
                return

            # found one bigger, so should be behind it
            if score < item:

                # create the item
                ri = RankItem(content, score)

                # insert in front of the previous item
                self._list.insert(i+1, ri)

                # game over
                return

    # clean
    def _clean(self):
        if len(self._list) > self._maxlen:
            self._list = self._list[:self._maxlen]

    # name
    @property
    def name(self) -> str:
        return self._name

    # contents
    @property
    def contents(self) -> List:
        self._clean()
        ret = [i.content for i in self._list]
        return ret

    # scores
    @property
    def scores(self) -> List:
        self._clean()
        ret = [i.score for i in self._list]
        return ret

    # rank items
    @property
    def rank_items(self) -> List[RankItem]:
        self._clean()
        return self._list

    # tuples
    @property
    def tuples(self) -> List[Tuple]:
        self._clean()
        ret = [(i.content, i.score) for i in self._list]
        return ret


def _tests():

    def not_vowel(c: str):
        return c not in 'aeiou'

    rank = Rank(name='test', maxlen=5, validate_fun=not_vowel)

    import string
    contents = list(string.ascii_lowercase[:18])
    scores = [-1, 10, 10, -2, 12, 12, 12, 8, 14, 8, 9, 11, 13, 16, 9, 0, 0, 10]

    print('contents')
    print(contents)
    print()
    print('scores')
    print(scores)
    print()

    print(50*'-')
    for i in range(len(contents)):
        print('pushed')
        print(f'content={contents[i]}, score={scores[i]}')
        print()

        rank.push(contents[i], scores[i])

        print(rank)
        print()
        print(50*'-')


# tests
if __name__ == '__main__':
    _tests()
