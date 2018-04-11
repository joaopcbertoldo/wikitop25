# -*- coding: utf-8 -*-
"""
rank.py
    This encapsulate the behavior associated with the ordering of a rank, which is done as the items are added.
    Defines classes RankItem and Rank (which is compose of the later).
    RankItem
        Associates a list of contents to a score, which is used to define its position in a Rank.
    Rank
        Manages a list of RankItem objects. Its main function is the push, which adds a content in the rank.
"""

from typing import List, Dict, Callable, Union
from numbers import Number


# Rank Item
class RankItem:
    """
    Stores a score (used to order the rank) and list of contents, as there might be several
    contents with the same score. "Content" is an abstraction of a thing that can be ranked
    (for the app, a page name).
    """

    # init
    def __init__(self, content, score):
        # store content and score internally, initializing the contents list
        self._contents = [content]
        self.score = score

    # add content
    def add_content(self, content):
        """Append a content to the rank item."""
        self._contents.append(content)

    # remove content
    def remove_content(self, content):
        """Remove a content from the rank item."""
        self._contents.remove(content)

    # contents
    @property
    def contents(self):
        """A list of contents in the rank item."""
        return self._contents

    # str - for debugging purposes
    def __str__(self):
        # get a str of the list of contents
        contents_str = str(self._contents)

        # limit the string's size
        contents_str = contents_str if len(contents_str) < 50 else contents_str[:50] + '...'

        # combine infos in a string
        return f'RankItem(score: {self.score}, contents({len(self._contents)}): {contents_str})'

    # all the method below here are for rank item logical comparisons
    # they can either be compared to 1) another item (with a score attribute) or 2) with Number
    # 1 -> scores are compared
    # 2 -> self's score is compared to the number

    # ==
    def __eq__(self, other) -> bool:
        return self.score == other if isinstance(other, Number) else self.score == other.score

    # !=
    def __ne__(self, other) -> bool:
        return self.score != other if isinstance(other, Number) else self.score != other.score

    # >
    def __gt__(self, other) -> bool:
        return self.score > other if isinstance(other, Number) else self.score > other.score

    # >=
    def __ge__(self, other) -> bool:
        return self.score >= other if isinstance(other, Number) else self.score >= other.score

    # <
    def __lt__(self, other) -> bool:
        return self.score < other if isinstance(other, Number) else self.score < other.score

    # <=
    def __le__(self, other) -> bool:
        return self.score <= other if isinstance(other, Number) else self.score <= other.score


# ------------------------------------------------ RANK ----------------------------------------------------------------
class Rank:
    """
    Stores an ordered list of things.
    The order is given by a score associated with the contents.
    The contents, when have the same score, are put in a same rank position.
    This hides the logic behind the ordering of a rank.
        The strategy is to rank contents as they are pushed into the rank.
        The internal list can surpass the max len, that's why there is _clean.
        Draws are add to the same rank item.
        Score is supposed to be in descendent order  (being 0 le plus petit).
    """

    # init
    def __init__(self, name: str, maxlen: int, validate_fun: Callable = None):
        """
        Just copy attributes and init the internal list of items.
        :param name: name of the rank (an alias, an id)
        :param maxlen: max number of rank items/size of the rank
        :param validate_fun: function that checks if a given content is valid
        """
        self._name = name
        self._maxlen = maxlen
        self._list: List[RankItem] = []
        self._validate_fun = validate_fun

    # len
    def __len__(self):
        """The len of the internal line or the maxlen (in case the list surpasses it)."""
        return min(len(self._list), self._maxlen)

    # [] operator
    def __getitem__(self, index) -> RankItem:
        """Get the rank item in position 'index', which corresponds to its rank position (starts on 0!!!!)."""
        return self._list[index]

    # str
    def __str__(self):
        # rank items in str
        strs = ['\t' + str(ri) for ri in self.rank_items]
        # add the rank's infos
        strs.insert(0, f'Rank(name: {self.name}, len: {len(self)} (max: {self._maxlen}))')
        # gather everything
        ret = '\n'.join(strs)
        return ret

    # first
    @property
    def first(self) -> Union[RankItem, None]:
        """First in the rank (the highest score, index 0)."""
        return self._list[0] if self._list else None

    # last
    @property
    def last(self) -> Union[RankItem, None]:
        """Last in the rank (the lowest score, index len - 1)."""
        return self._list[len(self) - 1] if self._list else None

    # has max len
    @property
    def has_max_len(self) -> bool:
        """Rather the rank has already its maximal length."""
        return len(self._list) >= self._maxlen

    # push
    def push(self, content, score):
        """
        Inserts a content in the rank.
        If score < lowest in the rank
            content ignored
        If score == some score in the the rank
            content is appended to the rank item
        If some score < score < other score
            a new rank item is created in the rank
                if len is already == maxlen, the last one is dropped out of the score

        Algorithm:
            the strategy is to compare the scores bottom-up, because whenever the last in the rank is
            bigger than the pushed content, there is no need to check the others (they are bigger too)
        """

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

        # algorithm to insert it inside the rank

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

    # post validate
    def post_validate(self, validate_fun):
        """Applies a validation function on all the contents in the rank items, eliminating them if not valid."""
        # check every rank item
        for ri in self._list:
            # look each content of the rank items
            for c in ri.contents:
                # if not valid
                if not validate_fun(c):
                    # remove it
                    ri.remove_content(c)

            # remove the item ended up empty and remove it if so
            if len(ri.contents) == 0:
                self._list.remove(ri)

    def resize(self, newmaxlen: int):
        """Change the maxlen of the rank."""
        self._maxlen = newmaxlen
        self._clean()

    # clean
    def _clean(self):
        """Drop every rank item after maxlen-1 from the internal list."""
        if len(self._list) > self._maxlen:
            self._list = self._list[:self._maxlen]

    # name
    @property
    def name(self) -> str:
        return self._name

    # rank items
    @property
    def rank_items(self) -> List[RankItem]:
        self._clean()
        return self._list

    # dictionized items
    @property
    def dictionized_items(self) -> List[Dict]:
        """
        A list of dicts for each item return with their:
            'ranked_pos' (the position in the rank, starting on 0 !!!!)
            'values' a list of its contents
            'score' its score
        """
        self._clean()
        ret = [{'ranked_pos': i, 'values': item.contents, 'score': item.score} for i, item in enumerate(self._list)]
        return ret


# test
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


# for test purposes
if __name__ == '__main__':
    _tests()
