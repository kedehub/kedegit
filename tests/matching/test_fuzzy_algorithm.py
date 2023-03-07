import numpy as np
import unittest
from unittest.mock import patch
from io import StringIO

from names_matcher.algorithm import NamesMatcher

class TestCreateIdentityMatcher(unittest.TestCase):

    def test_docstring(self):
        assignments = NamesMatcher()([["Vadim Markovtsev", "vmarkovtsev"], ["Long, Waren", "warenlg"]],
                                     [["Warren"], ["VMarkovtsev"], ["Eiso Kant"]])
        self.assertListEqual([1, 0], assignments[0].tolist())
        self.assertListEqual([1, 0.5882352941176471],assignments[1].tolist() )

    def test_compare_two_lists_1(self):

        names_1 = [["Warren"], ["VMarkovtsev"], ["Eiso Kant"]]
        names_2 = [["Vadim Markovtsev", "vmarkovtsev"], ["Long, Waren", "warenlg"]]


        assignments = NamesMatcher()(names_1,
                                     names_2)

        for counter, match in enumerate(assignments[0]):
            if match >= 0 and assignments[1][counter] > 0.5:
                names_1[match].extend(names_2[counter])
        self.assertListEqual([['Warren', 'Long, Waren', 'warenlg'], ['VMarkovtsev', 'Vadim Markovtsev', 'vmarkovtsev'], ['Eiso Kant']],
                             names_1)

    def test_compare_two_lists_2(self):

        names_1 = [["Vadim Markovtsev", "vmarkovtsev"], ["Long, Waren", "warenlg"]]
        names_2 = [["Warren"], ["VMarkovtsev"], ["Eiso Kant"]]

        assignments = NamesMatcher()(names_1,
                                     names_2)

        for counter, match in enumerate(assignments[0]):
            if match >= 0:
                names_1[match].extend(names_2[counter])

        self.assertListEqual([['Vadim Markovtsev', 'vmarkovtsev', 'VMarkovtsev'], ['Long, Waren', 'warenlg', 'Warren']],
                             names_1)

    def test_compare_same_list(self):

        names_1 = [["Vadim Markovtsev", "vmarkovtsev"], ["Long, Waren", "warenlg"]]
        names_2 = [["Vadim Markovtsev", "vmarkovtsev"], ["Long, Waren", "warenlg"]]

        assignments = NamesMatcher()(names_1,
                                     names_2)

        for counter, match in enumerate(assignments[0]):
            if match >= 0:
                names_1[match].extend(names_2[counter])

        self.assertListEqual([['Vadim Markovtsev', 'vmarkovtsev', 'Vadim Markovtsev', 'vmarkovtsev'], ['Long, Waren', 'warenlg', 'Long, Waren', 'warenlg']],
                             names_1)

    def test_compare_same_list_one_identity(self):

        names_1 = [["Vadim Markovtsev", "vmarkovtsev"]]
        names_2 = [["Vadim Markovtsev", "vmarkovtsev"]]

        assignments = NamesMatcher()(names_1,
                                     names_2)

        self.assertEqual(0,
                             assignments[0][0])
        self.assertEqual(1,
                             assignments[1][0])


    def test_compare_different_identities(self):

        names_1 = [["V", "v"]]
        names_2 = [["L", "o"]]

        assignments = NamesMatcher()(names_1,
                                     names_2)

        self.assertEqual(0, assignments[0][0])
        self.assertEqual(0, assignments[1][0])

    def test_reap_idenity(self):
        param_list = [
            [[], (set(), "")],
            [["VMarkovtsev", "vmarkovtsev"], ({"v", "markovtsev"}, "vmarkovtsev")],
            [["markovtsev", "ricardomarkovtsev"], ({"ricardo", "markovtsev"}, "markovtsevricardo")],
            [["ricard", "ricardomarkovtsev"], ({"ricard", "omarkovtsev"}, "ricardomarkovtsev")],
            [["Vadim_MARKOVTSEV (Rebase PR)"], ({"vadim", "markovtsev"}, "vadimmarkovtsev")],
            [["MarkõvtsevVádim"], ({"vadim", "markovtsev"}, "markovtsevvadim")],
        ]

        for names, result in param_list:
            with self.subTest():
                self.assertEqual(result, NamesMatcher().reap_identity(names) )

    def test_distance(self):
        param_list = [
            [({"a"}, "a"), ({"a"}, "a"), 0],
            [(set(), ""), (set(), ""), 1],
            [(set(), ""), ({"a"}, ""), 1],
            [({"a", "b"}, "ba"), ({"a", "c"}, "ca"), 1 / 3],
        ]

        for names1, names2, result in param_list:
            with self.subTest():
                self.assertAlmostEqual(result, NamesMatcher.distance(names1, names2))

    # # https://ryip.me/posts/python/unittest-stdout-stderr/
    # # The order of decorator is important!
    # @patch('sys.stdout', new_callable=StringIO)
    # @patch('sys.stderr', new_callable=StringIO)
    # def test_progress_on(self, stderr, stdout):
    #     NamesMatcher().match_parts(*([[({"%04d" % i}, "%04d" % i) for i in range(1000)]] * 2))
    #
    #     expected_err = ''
    #     self.assertEqual(stderr.getvalue(), expected_err)
    #
    # @patch('sys.stdout', new_callable=StringIO)
    # @patch('sys.stderr', new_callable=StringIO)
    # def test_progress_off(self, stderr, stdout):
    #     NamesMatcher().match_parts(*([[({"%04d" % i}, "%04d" % i) for i in range(1000)]] * 2),
    #                                disable_progress=True)
    #     expected_err = ''
    #     self.assertEqual(stderr.getvalue(), expected_err)


    def test_warning(self):
        with self.assertWarns(ResourceWarning):
            matrix = 1 - np.flip(np.eye(10000, dtype=np.float32), axis=0)
            NamesMatcher().solve_lap(matrix, len(matrix) // 2)
