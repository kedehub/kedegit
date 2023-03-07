import unittest
from pandas import DataFrame
from kedehub.services.template_finder import _make_table


class TemplateFinderTestCase(unittest.TestCase):

    def test_print_styled(self):

        df = DataFrame.from_dict( { 'repository':['azbg_virtual_pos','azbg_market_consent'],
                                    'hexsha': ['447fa6fdf974e784c45b004bfd7e84f5c68597bf', '0a18a71de33ff09fd04e7491ab580f39f7f88c03'],
                                   'added_chars': [352821.0, 441005.0],
                                    'deleted_chars': [0, 0],
                                   'chars_added_to_template': [0, 0]})
        expected_table = '+---------------------+------------------------------------------+-------------------------+---------------------------+\n' \
                        '| Repository          |            hexsha of the template commit | Added chars of template | Deleted chars of template |\n' \
                        '+---------------------+------------------------------------------+-------------------------+---------------------------+\n' \
                        '| azbg_market_consent | 0a18a71de33ff09fd04e7491ab580f39f7f88c03 |               [92m441,005.0[0m |                         [92m0[0m |\n' \
                        '+---------------------+------------------------------------------+-------------------------+---------------------------+\n' \
                        '| azbg_virtual_pos    | 447fa6fdf974e784c45b004bfd7e84f5c68597bf |               [92m352,821.0[0m |                         [92m0[0m |\n' \
                        '+---------------------+------------------------------------------+-------------------------+---------------------------+'
        self.assertEqual(expected_table, str(_make_table(df)))


def highlight_max(s):
    '''
    highlight the maximum in a Series yellow.
    '''
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]

if __name__ == '__main__':
    unittest.main()
