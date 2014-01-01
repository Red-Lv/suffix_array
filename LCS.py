#! /bin/env python
#! -*coding:GBK-*-

__author__ = 'lvleibing01'

import SuffixArraybyDC3


def binary_search(l, left, right, key):

    while left <= right:

        mid = (left + right) / 2

        if l[mid] <= key:
            left = mid + 1
        else:
            right = mid - 1

    return right


class LCS(object):

    def __init__(self):
        self.suffix_array = SuffixArraybyDC3.SuffixArraybyDC3()

        self.str_list = []
        self.sep = u'\u001a'
        self.start_index_list = []

    def init(self, *args):
        """
        """

        self.str_list = [list(_str) for _str in args]

        self.str_comp = self.sep.join(args)
        self.start_index_list.append(0)
        for _str in self.str_list:
            self.start_index_list.append(self.start_index_list[-1] + len(_str) + 1)
        self.start_index_list = self.start_index_list[: -1]

        self.suffix_array.init(self.str_comp)

        return True

    def exist_cs(self, k):
        """
        """

        str_cover_dict = {}
        for i in range(len(self.suffix_array.height_array)):

            if self.suffix_array.height_array[i] < k:
                str_cover_dict = {}
                continue

            pre_offset = self.suffix_array.SA[i - 1]
            offset = self.suffix_array.SA[i]

            str_index = binary_search(self.start_index_list, 0, len(self.start_index_list) - 1, pre_offset)
            str_cover_dict[str_index] = 1

            str_index = binary_search(self.start_index_list, 0, len(self.start_index_list) - 1, offset)
            str_cover_dict[str_index] = 1

            if len(str_cover_dict) >= len(self.str_list):
                return self.str_comp[self.suffix_array.SA[i]: ][: k]

        return None

    def gen_lcs(self):
        """
        """

        self.suffix_array.gen_height_array()
        #self.suffix_array.dump_suffix_array()
        #self.suffix_array.dump_height_array()

        min_len = min(map(len, self.str_list))
        left, right = 0, min_len

        lcs = None
        while left <= right:

            mid = (left + right) / 2
            cs = self.exist_cs(mid)
            if cs:
                lcs = cs
                l = mid + 1
            else:
                r = mid - 1

        print lcs

        return True

if __name__ == '__main__':

    lcs = LCS()

    str_list = [unicode('我们的内容内容内容简介：', 'GBK'), unicode('武动乾坤内容简介：', 'GBK')]
    lcs.init(*str_list)

    lcs.gen_lcs()
