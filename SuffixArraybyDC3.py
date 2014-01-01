#! /bin/env python
#! -*coding:UTF-8-*-

__author__ = 'lvleibing01'

import itertools


class SuffixArraybyDC3(object):

    def __init__(self):

        pass

    def init(self, s, K):

        self.s = s
        if isinstance(self.s, str):
            self.s = list(self.s)

        self.s = [ord(item) for item in s]

        self.K = K

        self.SA = []
        self.LCP = []

        return True

    def radix_sort(self, index_arr, ori_arr, K):
        """radix sort

        Arguments:
            index_arr:  subsequence of [0, 1, ... len(ori_arr)]
            ori_arr:    ori array
            K:  the element in ori_arr belongs to [0, K]
        """

        index_arr_len = len(index_arr)
        count = [0] * (K + 1)

        for i in xrange(index_arr_len):

            index = index_arr[i]
            count[ori_arr[index]] += 1

        _sum = 0
        for i in xrange(0, K + 1):
            count[i], _sum = _sum, count[i] + _sum

        index_arr_sorted = [None] * index_arr_len
        for i in range(index_arr_len):

            index = index_arr[i]

            index_arr_sorted[count[ori_arr[index]]] = index
            count[ori_arr[index]] += 1

        return index_arr_sorted

    def _gen_suffix_array(self, s, K):
        """
        """

        n = len(s)
        s.extend([0] * 3)

        #the count of element mod 3 == 0, 1, 2
        n0, n1, n2 = (n + 2) / 3, (n + 1) / 3, n / 3

        #index in [0, n) where position % 3 == 1
        #why n0 - n1:
        #   if (n - 1) % 3 == 0, the n % 3 == 1.
        #   so we need n in SA12 in the step 3: merging S0 with S12
        s12 = []
        for i in xrange(n + n0 - n1):
            if i % 3 != 0:
                s12.append(i)

        #sort the three element tuple starting at s12[0, 1, ... len(s12))
        SA12 = self.radix_sort(s12, s[2:], K)
        s12 = self.radix_sort(SA12, s[1:], K)
        SA12 = self.radix_sort(s12, s[0:], K)

        c0 = c1 = c2 = None
        count = -1
        for i in xrange(len(SA12)):

            index = SA12[i]
            if s[index] != c0 or s[index + 1] != c1 or s[index + 2] != c2:
                count += 1
                c0, c1, c2 = s[index: index + 3]

            if index % 3 == 1:
                s12[index / 3] = count
            else:
                #why n0 rather than n1?
                #   Because n0 is more significant than n1, for sometimes we need include n in the s12
                s12[index / 3 + n0] = count

        if count != len(s12) - 1:
            #recursive
            SA12 = self._gen_suffix_array(s12, K)
            #gen the s12 from SA12
            for i, index in enumerate(SA12):
                s12[index] = i
        else:
            #gen the SA from s12
            for i, index in enumerate(s12):
                SA12[index] = i

        #excellent idea. enjoy this
        s0 = [index * 3 for index in SA12 if index < n1]
        SA0 = self.radix_sort(s0, s, K)

        def get_index_of_s_for_s12(index, n0):

            if index < n1:
                return index * 3 + 1
            else:
                return (index - n0) * 3 + 2

        SA12 = map(lambda index: index * 3 + 1 if index < n0 else (index - n0) * 3 + 2, SA12)
        #why?
        #   pay attention to the step three: merging SA0 with SA12
        #   the None acts as a sentinel
        s12.append(None)

        SA = []
        #excellent trick
        i, j = 0,  n0 - n1
        while i < n0 and j < n0 + n2:

            index_0 = SA0[i]
            index_12 = SA12[j]

            def leq(t1, t2):

                for a, b in itertools.izip(t1, t2):
                    if a < b:
                        return True
                    if a > b:
                        return False

                return True

            if (leq((s[index_0], s12[(index_0 + 1) / 3]),
                    (s[index_12], s12[n0 + (index_12 + 1) / 3])) if index_12 % 3 == 1
                    else leq((s[index_0], s[index_0 + 1], s12[index_0 / 3 + n0]),
                             (s[index_12], s[index_12 + 1], s12[(index_12 + 2) / 3]))):

                SA.append(index_0)
                i += 1
            else:
                SA.append(index_12)
                j += 1
        else:

            if i < n0:
                SA.extend(SA0[i: n0])

            if j < n0 + n2:
                SA.extend(SA12[j: n0])

        return SA

    def gen_suffix_array(self):
        """
        """

        self.SA = self._gen_suffix_array(self.s[:], self.K)

    def 

    def dump_suffix_array(self):
        """
        """

        for i in xrange(len(self.SA)):
            suffix = ''.join(map(chr,self.s[self.SA[i]: ]))
            print '\t'.join(map(str, [i, self.SA[i], suffix]))

if __name__ == '__main__':

    suffix_array_dc3 = SuffixArraybyDC3()
    suffix_array_dc3.init('bacacbefghibcefghi', 128)

    suffix_array_dc3.gen_suffix_array()

    suffix_array_dc3.dump_suffix_array()
