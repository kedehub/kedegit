import unittest
from Levenshtein import editops
from kedehub.gitclient.levenshtein_utility import LINE_DELETED_KEY, LINE_ADDED_KEY, \
    find_added_deleted_chars_in_hunk
from unidiff.patch import (
    LINE_TYPE_ADDED,
    LINE_TYPE_CONTEXT,
    LINE_TYPE_REMOVED,
    Line, Hunk,
)

class LevenshteinTestCase(unittest.TestCase):

    def test_editops(self):
        ops = editops('spam', 'park')

        self.assertEqual(('delete', 0, 0), ops[0])
        self.assertEqual(('insert', 3, 2), ops[1])
        self.assertEqual(('replace', 3, 3), ops[2])

    def test_editops_empty_strings(self):
        ops = editops('', '')

        self.assertEqual(0, len(ops))

    def test_editops_one_replaced_char(self):
        ops = editops('contract.storage[1000] = 0', 'contract.storage[1000] = 1')

        self.assertEqual(('replace', 25, 25), ops[0])

    def test_editops_small_into_large_caps_chars(self):
        ops = editops('contract.storage[mycreator] = 10^18', 'contract.storage[MYCREATOR] = 10^18')

        self.assertEqual(9,len(ops))
        self.assertListEqual([('replace', 17, 17), ('replace', 18, 18), ('replace', 19, 19), ('replace', 20, 20), ('replace', 21, 21), ('replace', 22, 22), ('replace', 23, 23), ('replace', 24, 24), ('replace', 25, 25)],
                             ops)

    def test_find_added_deleted_chars(self):
        added_line = Line('Sample line', line_type=LINE_TYPE_ADDED)
        removed_line = Line('Sample line', line_type=LINE_TYPE_REMOVED)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(removed_line)
        hunk.append(added_line)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(0, counter[LINE_DELETED_KEY])
        self.assertEqual(0, counter[LINE_ADDED_KEY])

    def test_find_added_deleted_chars_one_replaced_char(self):
        added_line = Line('contract.storage[1000] = 0', line_type=LINE_TYPE_ADDED)
        removed_line = Line('contract.storage[1000] = 1', line_type=LINE_TYPE_REMOVED)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(removed_line)
        hunk.append(added_line)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(1, counter[LINE_DELETED_KEY])
        self.assertEqual(1, counter[LINE_ADDED_KEY])

    def test_find_added_deleted_chars_small_into_large_caps_chars(self):
        added_line = Line('contract.storage[mycreator] = 10^18', line_type=LINE_TYPE_ADDED)
        removed_line = Line('contract.storage[MYCREATOR] = 10^18', line_type=LINE_TYPE_REMOVED)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(removed_line)
        hunk.append(added_line)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(9, counter[LINE_DELETED_KEY])
        self.assertEqual(9, counter[LINE_ADDED_KEY])

    def test_find_find_added_deleted_only_added_chars_1(self):
        '''
        We have aonly aded chars even though diff says there are deleted lines

        Source: https://github.com/ethereum/wiki/commit/ca8b34c417631a35c899d6a4d466c0447fd2e381.patch

-            mktx(contract.storage[1003],ethervalue,0,0)
-            mktx(A,5000 - ethervalue,0,0)
+            mktx(contract.storage[1003],ethervalue * 10^18,0,0)
+            mktx(A,(5000 - ethervalue) * 10^18,0,0)
        '''
        removed_line_1 = Line('mktx(contract.storage[1003],ethervalue,0,0)', line_type=LINE_TYPE_REMOVED)
        removed_line_2 = Line('mktx(A,5000 - ethervalue,0,0)', line_type=LINE_TYPE_REMOVED)
        added_line_1 = Line('mktx(contract.storage[1003],ethervalue * 10^18,0,0)', line_type=LINE_TYPE_ADDED)
        added_line_2 = Line('mktx(A,(5000 - ethervalue) * 10^18,0,0)', line_type=LINE_TYPE_ADDED)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(removed_line_1)
        hunk.append(removed_line_2)
        hunk.append(added_line_1)
        hunk.append(added_line_2)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(0, counter[LINE_DELETED_KEY])
        self.assertEqual(18, counter[LINE_ADDED_KEY])

    def test_find_find_added_deleted_only_deleted(self):
        '''
        We have only deleted chars.

        Source: https://github.com/ethereum/wiki/commit/98d9a27144cac3b4f7c59c0e89c6b59e35a49a10

            @@ -14,10 +14,9 @@ A full block is stored as:
             Where:

                 transaction_list = [
            -        transaction 0, medstate 0, stkhash 0, subhash 0],
            +        transaction 0,
                     transaction 1,
                     ...
            -        transaction n,
                 ]

                 uncle list = [
        '''
        removed_line_1 = Line('transaction 0, medstate 0, stkhash 0, subhash 0],', line_type=LINE_TYPE_REMOVED)
        removed_line_2 = Line('transaction n,', line_type=LINE_TYPE_REMOVED)
        added_line_1 = Line('transaction 0,', line_type=LINE_TYPE_ADDED)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(removed_line_1)
        hunk.append(removed_line_2)
        hunk.append(added_line_1)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(49, counter[LINE_DELETED_KEY])
        self.assertEqual(0, counter[LINE_ADDED_KEY])

    def test_find_find_added_deleted_more_chars_than_added(self):
        '''
        We have deleted more chars than we have added.

        Source: https://github.com/ethereum/wiki/commit/98d9a27144cac3b4f7c59c0e89c6b59e35a49a10

            @@ -144,7 +142,7 @@ When mining a block, a miner goes through the following process:
             * Apply the transaction `TRIETOP(txstack)` to `state`.
             * `TRIEPOP(txstack)`
             * Let `L[0] ... L[m-1]` be the list of new transactions spawned by that transaction via `MKTX`, in the order that they were produced during script execution.
            -* Initialize `j = m-1`. While `j &gt;= 0`, `TRIEPUSH(txstack,L[j])` and `j -= 1`
            +* Initialize `j = m-1`. While `j >= 0`, `TRIEPUSH(txstack,L[j])` and `j -= 1`

             5- Make the following modifications to the state tree:
        '''
        removed_line_1 = Line('* Initialize `j = m-1`. While `j &gt;= 0`, `TRIEPUSH(txstack,L[j])` and `j -= 1`', line_type=LINE_TYPE_REMOVED)
        added_line_1 = Line('* Initialize `j = m-1`. While `j >= 0`, `TRIEPUSH(txstack,L[j])` and `j -= 1`', line_type=LINE_TYPE_ADDED)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(removed_line_1)
        hunk.append(added_line_1)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(4, counter[LINE_DELETED_KEY])
        self.assertEqual(1, counter[LINE_ADDED_KEY])

    def test_find_find_added_deleted_less_chars_than_added(self):
        '''
        We have deleted less chars than we have added.

        Source: https://github.com/ethereum/aleth/commit/d1b93ed468ffc3d1766f5cb7dc1e47f14b4dd67a

            @@ -2,9 +2,9 @@
             #define MAIN_H

             #include <QtNetwork/QNetworkAccessManager>
            -#include <QAbstractListModel>
            -#include <QMainWindow>
            -#include <QMutex>
            +#include <QtCore/QAbstractListModel>
            +#include <QtCore/QMutex>
            +#include <QtWidgets/QMainWindow>
             #include <libethereum/Common.h>

             namespace Ui {
        '''
        removed_line_1 = Line('#include <QAbstractListModel>', line_type=LINE_TYPE_REMOVED)
        removed_line_2 = Line('#include <QMainWindow>', line_type=LINE_TYPE_REMOVED)
        removed_line_3 = Line('#include <QMutex>', line_type=LINE_TYPE_REMOVED)
        added_line_1 = Line('#include <QtCore/QAbstractListModel>', line_type=LINE_TYPE_ADDED)
        added_line_2 = Line('#include <QtCore/QMutex>', line_type=LINE_TYPE_ADDED)
        added_line_3 = Line('#include <QtWidgets/QMainWindow>', line_type=LINE_TYPE_ADDED)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(removed_line_1)
        hunk.append(removed_line_2)
        hunk.append(removed_line_3)
        hunk.append(added_line_1)
        hunk.append(added_line_2)
        hunk.append(added_line_3)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(14, counter[LINE_DELETED_KEY])
        self.assertEqual(38, counter[LINE_ADDED_KEY])

    def test_find_find_added_deleted_only_added_chars_2(self):
        '''
        We have only added chars.

        Source: https://github.com/ethereum/aleth/commit/87e19602ea46cb3b0ed3cdee7b27aad33276705a

            @@ -21,6 +21,7 @@

             #include "Common.h"

            +#include <fstream>
             #include <random>
             #if WIN32
             #pragma warning(push)
        '''

        added_line_1 = Line('#include <fstream>', line_type=LINE_TYPE_ADDED)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(added_line_1)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(0, counter[LINE_DELETED_KEY])
        self.assertEqual(18, counter[LINE_ADDED_KEY])

    def test_find_added_deleted_chars_one_replaced_char_surounded_by_context_lines(self):
        added_line = Line('contract.storage[1000] = 0', line_type=LINE_TYPE_ADDED)
        removed_line = Line('contract.storage[1000] = 1', line_type=LINE_TYPE_REMOVED)
        context_line = Line('xxx', line_type=LINE_TYPE_CONTEXT)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(context_line)
        hunk.append(removed_line)
        hunk.append(added_line)
        hunk.append(context_line)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(1, counter[LINE_DELETED_KEY])
        self.assertEqual(1, counter[LINE_ADDED_KEY])

    def test_find_added_deleted_chars_small_into_large_caps_chars_surounded_by_context_lines(self):
        added_line = Line('contract.storage[mycreator] = 10^18', line_type=LINE_TYPE_ADDED)
        removed_line = Line('contract.storage[MYCREATOR] = 10^18', line_type=LINE_TYPE_REMOVED)
        context_line = Line('xxx', line_type=LINE_TYPE_CONTEXT)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(context_line)
        hunk.append(removed_line)
        hunk.append(added_line)
        hunk.append(context_line)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(9, counter[LINE_DELETED_KEY])
        self.assertEqual(9, counter[LINE_ADDED_KEY])

    def test_find_added_deleted_chars_from_samples_pom_xml(self):
        # the source is samples/pom.xml.diff
        context_line_1 = Line('	<relativePath/> <!-- lookup parent from repository -->', line_type=LINE_TYPE_CONTEXT)
        context_line_2 = Line('</parent>', line_type=LINE_TYPE_CONTEXT)
        context_line_3 = Line('<groupId>bg.allianz</groupId>', line_type=LINE_TYPE_CONTEXT)
        removed_line_1 = Line('<artifactId>marketing.consent</artifactId>', line_type=LINE_TYPE_REMOVED)
        added_line_1 = Line('<artifactId>virtualpos.adapter</artifactId>', line_type=LINE_TYPE_ADDED)
        context_line_4 = Line('<version>0.0.1-SNAPSHOT</version>', line_type=LINE_TYPE_CONTEXT)
        removed_line_2 = Line('<name>marketing.consent</name>', line_type=LINE_TYPE_REMOVED)
        removed_line_3 = Line('<description>Marketing consent app</description>', line_type=LINE_TYPE_REMOVED)
        added_line_2 = Line('<name>virtualpos.adapter</name>', line_type=LINE_TYPE_ADDED)
        added_line_3 = Line('<description>Virtaul PoS adapter</description>', line_type=LINE_TYPE_ADDED)
        context_line_5 = Line('', line_type=LINE_TYPE_CONTEXT)
        context_line_6 = Line('<properties>', line_type=LINE_TYPE_CONTEXT)
        context_line_7 = Line('	<java.version>1.8</java.version>', line_type=LINE_TYPE_CONTEXT)

        hunk = Hunk(src_len=None, tgt_len=None)
        hunk.append(context_line_1)
        hunk.append(context_line_2)
        hunk.append(context_line_3)
        hunk.append(removed_line_1)
        hunk.append(added_line_1)
        hunk.append(context_line_4)
        hunk.append(removed_line_2)
        hunk.append(removed_line_3)
        hunk.append(added_line_2)
        hunk.append(added_line_3)
        hunk.append(context_line_5)
        hunk.append(context_line_6)
        hunk.append(context_line_7)

        counter = find_added_deleted_chars_in_hunk(hunk)
        self.assertEqual(45, counter[LINE_DELETED_KEY])
        self.assertEqual(45, counter[LINE_ADDED_KEY])

if __name__ == '__main__':
    unittest.main()
