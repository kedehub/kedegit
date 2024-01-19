import unittest

from pandas import DataFrame, read_json
from pandas._testing import assert_frame_equal, assert_index_equal, assert_numpy_array_equal
from io import StringIO

class KedeGitTestJson(unittest.TestCase):
    def test_read_json(self):
        df = DataFrame([['a', 'b'], ['c', 'd']],
                       index=['index " 1', 'index / 2'],
                       columns=['a \\ b', 'y / z'])

        assert_frame_equal(df, read_json(StringIO(df.to_json(orient='split')),
                                         orient='split'))
        assert_frame_equal(df, read_json(StringIO(df.to_json(orient='columns')),
                                         orient='columns'))
        assert_frame_equal(df, read_json(StringIO(df.to_json(orient='index')),
                                         orient='index'))
        df_unser = read_json(StringIO(df.to_json(orient='records')), orient='records')
        assert_index_equal(df.columns, df_unser.columns)
        assert_numpy_array_equal(df.values, df_unser.values)

    def test_frame_from_json_bad_data_key(self):
        with self.assertRaises(ValueError, msg='Expected object or value'):
            read_json(StringIO('{"key":b:a:d}'))

    def test_frame_from_json_bad_data_too_few_indices(self):
        # too few indices
        json = StringIO('{"columns":["A","B"],'
                        '"index":["2","3"],'
                        '"data":[[1.0,"1"],[2.0,"2"],[null,"3"]]}')
        msg = r"Shape of passed values is \(3, 2\), indices imply \(2, 2\)"
        with self.assertRaises(ValueError, msg=msg):
            read_json(json, orient="split")

    def test_frame_from_json_bad_data_too_many_columns(self):
        # too many columns
        json = StringIO('{"columns":["A","B","C"],'
                        '"index":["1","2","3"],'
                        '"data":[[1.0,"1"],[2.0,"2"],[null,"3"]]}')
        msg = "3 columns passed, passed data had 2 columns"
        with self.assertRaises(ValueError, msg=msg):
            read_json(json, orient="split")

    def test_frame_from_json_bad_data_bad_key(self):
        # bad key
        json = StringIO('{"badkey":["A","B"],'
                        '"index":["2","3"],'
                        '"data":[[1.0,"1"],[2.0,"2"],[null,"3"]]}')
        with self.assertRaises(ValueError, msg=r"unexpected key\(s\): badkey"):
            read_json(json, orient="split")

    def test_frame_from_json_bad_data_too_few_indices_big(self):
        # too few indices
        json = StringIO('{"columns":["added_chars","hexsha","repository_path"],'
                        '"index":[["Jordan Radev <jordan.radev@elando.bg>",1589387361000],["Jordan Radev <jordan.radev@elando.bg>",1589354945000],["Jordan Radev <jordan.radev@elando.bg>",1589268906000],["Jordan Radev <jordan.radev@elando.bg>",1589384220000],["Jordan Radev <jordan.radev@elando.bg>",1593169908000],["Jordan Radev <jordan.radev@elando.bg>",1593175220000],["Jordan Radev <jordan.radev@elando.bg>",1593179607000],["Jordan Radev <jordan.radev@elando.bg>",1589815980000],["Jordan Radev <jordan.radev@elando.bg>",1589203908000],["Jordan Radev <jordan.radev@elando.bg>",1589815187000],["Jordan Radev <jordan.radev@elando.bg>",1589811316000],["Jordan Radev <jordan.radev@elando.bg>",1589804590000],["Jordan Radev <jordan.radev@elando.bg>",1589982603000],["Jordan Radev <jordan.radev@elando.bg>",1589186902000],["Jordan Radev <jordan.radev@elando.bg>",1590588426000],["Jordan Radev <jordan.radev@elando.bg>",1590587247000],["Jordan Radev <jordan.radev@elando.bg>",1590596643000],["Jordan Radev <jordan.radev@elando.bg>",1590594375000]],'
                        '"data":[[224,"15752b9916dace117f851da0fb13908cb422ee0d","\/Users\/dimitarbakardzhiev\/git\/azbg_virtual_pos"],[0,"6eca86ff0c76ee47660f7de19e615b0c3e4fe51f","\/Users\/dimitarbakardzhiev\/git\/azbg_virtual_pos"],[279,"bc09144732492461d63146461d724e62a4b33087","\/Users\/dimitarbakardzhiev\/git\/azbg_virtual_pos"],[745,"fdad1f0a41b22e6715a20813e968d25c7636a6a7","\/Users\/dimitarbakardzhiev\/git\/azbg_virtual_pos"],[8479,"2945c17c5db0cd2a92a8f4d6b738fcfa6a5e2122","\/Users\/dimitarbakardzhiev\/git\/azbg_onko_calc"],[0,"430c5016ef294e0b1a6aeded6c873cb56b19355c","\/Users\/dimitarbakardzhiev\/git\/azbg_onko_calc"],[0,"44dcb4e7e2a24dbeeb8daf036ff46ccfc6b623b0","\/Users\/dimitarbakardzhiev\/git\/azbg_onko_calc"],[417,"1010b3221841027117cf162f7bf801c74763bf92","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],[0,"524ad08d6d61b7ddf7b9fb02a330c04df3837ad1","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],[1546,"8b0bfffd571c685e6141e16aac9f5d6d5e1065b2","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],[1586,"a0ad65c9670d23cd42dfa73954c955d3d72c73b4","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],[10942,"a2a260f388f7443c0abbdf5c78ed9f24d7e1a28a","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],[0,"c7a93151242b30d2aff616a3b96233804c37e085","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],[437,"de2ad2d61fb31467c7cf26fb0a923f2372b5fadd","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],[1308,"2ccdc0edcbf7ef12e44a9eedbbc2fdae8fa1f9cb","\/Users\/dimitarbakardzhiev\/git\/azbg_digital_health_id"],[8523,"537a3ecc98169f6b8967ab900daec6ee72649c77","\/Users\/dimitarbakardzhiev\/git\/azbg_digital_health_id"],[0,"6cc539d3f8e8c42f83f2693b5d326eb53101d072","\/Users\/dimitarbakardzhiev\/git\/azbg_digital_health_id"],[231,"870e3e329a7a9a40b2c212824834e8603a78ed9c","\/Users\/dimitarbakardzhiev\/git\/azbg_digital_health_id"]]}')
        msg = r"Shape of passed values is \(18, 3\), indices imply \(2, 3\)"
        with self.assertRaises(ValueError, msg=msg):
            read_json(json, orient="split")

    def test_frame_from_json_data_split_no_indeces(self):
        # too few indices
        json = StringIO('{"columns":["author_name","commit_time","added_chars","hexsha","repository_path"],'
                        '"index":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],'
                        '"data":[["Jordan Radev <jordan.radev@elando.bg>",1589387361000,224,"15752b9916dace117f851da0fb13908cb422ee0d","\/Users\/dimitarbakardzhiev\/git\/azbg_virtual_pos"],["Jordan Radev <jordan.radev@elando.bg>",1589354945000,0,"6eca86ff0c76ee47660f7de19e615b0c3e4fe51f","\/Users\/dimitarbakardzhiev\/git\/azbg_virtual_pos"],["Jordan Radev <jordan.radev@elando.bg>",1589268906000,279,"bc09144732492461d63146461d724e62a4b33087","\/Users\/dimitarbakardzhiev\/git\/azbg_virtual_pos"],["Jordan Radev <jordan.radev@elando.bg>",1589384220000,745,"fdad1f0a41b22e6715a20813e968d25c7636a6a7","\/Users\/dimitarbakardzhiev\/git\/azbg_virtual_pos"],["Jordan Radev <jordan.radev@elando.bg>",1593169908000,8479,"2945c17c5db0cd2a92a8f4d6b738fcfa6a5e2122","\/Users\/dimitarbakardzhiev\/git\/azbg_onko_calc"],["Jordan Radev <jordan.radev@elando.bg>",1593175220000,0,"430c5016ef294e0b1a6aeded6c873cb56b19355c","\/Users\/dimitarbakardzhiev\/git\/azbg_onko_calc"],["Jordan Radev <jordan.radev@elando.bg>",1593179607000,0,"44dcb4e7e2a24dbeeb8daf036ff46ccfc6b623b0","\/Users\/dimitarbakardzhiev\/git\/azbg_onko_calc"],["Jordan Radev <jordan.radev@elando.bg>",1589815980000,417,"1010b3221841027117cf162f7bf801c74763bf92","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],["Jordan Radev <jordan.radev@elando.bg>",1589203908000,0,"524ad08d6d61b7ddf7b9fb02a330c04df3837ad1","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],["Jordan Radev <jordan.radev@elando.bg>",1589815187000,1546,"8b0bfffd571c685e6141e16aac9f5d6d5e1065b2","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],["Jordan Radev <jordan.radev@elando.bg>",1589811316000,1586,"a0ad65c9670d23cd42dfa73954c955d3d72c73b4","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],["Jordan Radev <jordan.radev@elando.bg>",1589804590000,10942,"a2a260f388f7443c0abbdf5c78ed9f24d7e1a28a","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],["Jordan Radev <jordan.radev@elando.bg>",1589982603000,0,"c7a93151242b30d2aff616a3b96233804c37e085","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],["Jordan Radev <jordan.radev@elando.bg>",1589186902000,437,"de2ad2d61fb31467c7cf26fb0a923f2372b5fadd","\/Users\/dimitarbakardzhiev\/git\/azbg_market_consent"],["Jordan Radev <jordan.radev@elando.bg>",1590588426000,1308,"2ccdc0edcbf7ef12e44a9eedbbc2fdae8fa1f9cb","\/Users\/dimitarbakardzhiev\/git\/azbg_digital_health_id"],["Jordan Radev <jordan.radev@elando.bg>",1590587247000,8523,"537a3ecc98169f6b8967ab900daec6ee72649c77","\/Users\/dimitarbakardzhiev\/git\/azbg_digital_health_id"],["Jordan Radev <jordan.radev@elando.bg>",1590596643000,0,"6cc539d3f8e8c42f83f2693b5d326eb53101d072","\/Users\/dimitarbakardzhiev\/git\/azbg_digital_health_id"],["Jordan Radev <jordan.radev@elando.bg>",1590594375000,231,"870e3e329a7a9a40b2c212824834e8603a78ed9c","\/Users\/dimitarbakardzhiev\/git\/azbg_digital_health_id"]]}')
        df = read_json(json, orient="split")
        df.set_index(['author_name', 'commit_time'], inplace=True)
        self.assertListEqual(['author_name', 'commit_time'], df.index.names)

if __name__ == '__main__':
    unittest.main()
