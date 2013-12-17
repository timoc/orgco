"""
orgco

Copyright (c) 2013, Friedrich Paetzke (f.paetzke@gmail.com)
All rights reserved.

"""
import os
import unittest

from orgco import convert_html
from orgco.convert import convert, find_markup
from orgco.orgalyzer import OrgDoc


def load_data(filename):
    test_data = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    filename = os.path.join(test_data, 'tests/data', filename)
    with open(filename, 'r') as f:
        return f.read()


def load(filename):
    return load_data(filename).split('\n')


class TestFindMarkup(unittest.TestCase):

    def test_regard_return_as_space(self):
        markup, i = find_markup('[[Some link]]\r', 0)
        self.assertEqual(i, 13)
        self.assertEqual(markup, '[[Some link]]')

    def test_minimum_markup_length(self):
        markup, i = find_markup('c++', 0)
        self.assertEqual(markup, 'c')
        self.assertEqual(i, 1)

        markup, i = find_markup('c++', i)
        self.assertEqual(markup, '+')
        self.assertEqual(i, 2)

    def test_colon_after_markup(self):
        markup, i = find_markup('/bold/: bool, default False', 0)
        self.assertEqual(markup, '/bold/')
        self.assertEqual(i, 6)


class TestOrgDoc(unittest.TestCase):

    def test_code00(self):
        org = OrgDoc(load_data('code00.org'))
        expected = '(defun org-xor (a b)\n  "Exclusive or."\n  (if a (not b) b))'
        self.assertEqual(len(org.things), 1)
        self.assertEqual(org.things[0].language, 'emacs-lisp')
        self.assertEqual(str(org.things[0]), expected)

    def test_definition00(self):
        org = OrgDoc(load_data('definition00.org'))

        self.assertEqual(len(org.things), 1)
        self.assertEqual(len(org.things[0].things), 3)
        self.assertEqual(org.things[0].things[0].term, 'short1')
        self.assertEqual(org.things[0].things[0].description, 'long1')
        self.assertEqual(org.things[0].things[1].term, 'short2')
        self.assertEqual(org.things[0].things[1].description, 'long2')
        self.assertEqual(org.things[0].things[2].term, 'short3')
        self.assertEqual(org.things[0].things[2].description, 'long3')

    def test_definition01(self):
        org = OrgDoc(load_data('definition01.org'))

        self.assertEqual(len(org.things), 1)
        self.assertEqual(len(org.things[0].things), 3)
        self.assertEqual(len(org.things[0].things[1].things), 4)

    def test_header00(self):
        org = OrgDoc(load_data('header00.org'))

        self.assertEqual(len(org.things), 1)
        self.assertEqual(org.things[0].level, 1)
        self.assertEqual(org.things[0].text, 'header1')

    def test_header01(self):
        org = OrgDoc(load_data('header01.org'))

        self.assertEqual(len(org.things), 3)
        self.assertEqual(org.things[0].level, 1)
        self.assertEqual(org.things[0].text, 'header11')
        self.assertEqual(org.things[1].level, 1)
        self.assertEqual(org.things[1].text, 'header12')
        self.assertEqual(org.things[2].level, 2)
        self.assertEqual(org.things[2].text, 'header21')

    def test_list00(self):
        org = OrgDoc(load_data('list00.org'))

        self.assertEqual(len(org.things), 1)
        self.assertEqual(len(org.things[0].things), 3)
        self.assertEqual(str(org.things[0].things[0]), 'item1')
        self.assertEqual(str(org.things[0].things[1]), 'item2')
        self.assertEqual(str(org.things[0].things[2]), 'item3')

    def test_list02(self):
        org = OrgDoc(load_data('list02.org'))

        self.assertEqual(len(org.things), 1)
        lst = org.things[0]
        self.assertEqual(len(lst.things), 7)
        self.assertEqual(len(lst.things[1].things), 2)
        self.assertEqual(len(lst.things[4].things), 2)
        self.assertEqual(len(lst.things[6].things), 1)

    def test_list03(self):
        org = OrgDoc(load_data('list03.org'))

        self.assertEqual(len(org.things), 1)
        lst = org.things[0]
        self.assertTrue(lst.ordered)
        self.assertEqual(len(lst.things), 4)
        self.assertEqual(str(lst.things[0]), 'item1')
        self.assertEqual(str(lst.things[1]), 'item2')
        self.assertEqual(str(lst.things[2]), 'item3')
        self.assertEqual(str(lst.things[3]), 'item4')

    def test_paragraph00(self):
        org = OrgDoc(load_data('paragraph00.org'))

        self.assertEqual(len(org.things), 4)
        self.assertEqual(len(org.things[0].lines), 4)
        self.assertEqual(len(org.things[1].lines), 6)
        self.assertEqual(len(org.things[2].lines), 6)
        self.assertEqual(len(org.things[3].lines), 6)

    def test_table00(self):
        org = OrgDoc(load_data('table00.org'))

        self.assertEqual(len(org.things), 1)
        table = org.things[0]
        self.assertEqual(len(table.things), 2)
        self.assertEqual(table.things[0].cols[0], 'td11')
        self.assertEqual(table.things[0].cols[1], 'td12')
        self.assertEqual(table.things[1].cols[0], 'td21')
        self.assertEqual(table.things[1].cols[1], 'td22')

    def test_table01(self):
        org = OrgDoc(load_data('table01.org'))

        self.assertEqual(len(org.things), 2)
        self.assertEqual(len(org.things[0].things), 2)
        self.assertEqual(len(org.things[1].things), 2)

    def test_table02(self):
        org = OrgDoc(load_data('table02.org'))

        self.assertEqual(len(org.things), 3)
        self.assertEqual(len(org.things[0].things), 2)
        self.assertEqual(len(org.things[1].things), 3)
        self.assertEqual(len(org.things[2].things), 2)

    def test_table03(self):
        org = OrgDoc(load_data('table03.org'))

        self.assertEqual(len(org.things), 1)
        self.assertEqual(len(org.things[0].things), 2)
        self.assertEqual(org.things[0].things[0].is_header, True)
        self.assertEqual(org.things[0].things[0].cols[0], 'th1')
        self.assertEqual(org.things[0].things[0].cols[1], 'th2')
        self.assertEqual(org.things[0].things[1].is_header, False)
        self.assertEqual(org.things[0].things[1].cols[0], 'td1')
        self.assertEqual(org.things[0].things[1].cols[1], 'td2')


class TestHtml(unittest.TestCase):

    def assertOrgAndHtmlEqual(self, orgfile, htmlfile):
        html = convert(OrgDoc(load_data(orgfile)), 'html')
        expected = load(htmlfile)
        self.assertEqual(html, expected)

    def test_definition01(self):
        self.assertOrgAndHtmlEqual('definition01.org', 'definition01.html')

    def test_header00(self):
        html = convert(OrgDoc(load_data('header00.org')), 'html')
        expected = ['<h1>header1</h1>', '']
        self.assertEqual(html, expected)

    def test_header01(self):
        self.assertOrgAndHtmlEqual('header01.org', 'header01.html')

    def test_list01(self):
        self.assertOrgAndHtmlEqual('list01.org', 'list01.html')

    def test_list03(self):
        self.assertOrgAndHtmlEqual('list03.org', 'list03.html')

    def test_list04(self):
        self.assertOrgAndHtmlEqual('list04.org', 'list04.html')

    def test_list05(self):
        self.assertOrgAndHtmlEqual('list05.org', 'list05.html')

    def test_list06(self):
        self.assertOrgAndHtmlEqual('list06.org', 'list06.html')

    def test_list07(self):
        self.assertOrgAndHtmlEqual('list07.org', 'list07.html')

    def test_paragraph00(self):
        self.assertOrgAndHtmlEqual('paragraph00.org', 'paragraph00.html')

    def test_paragraph01(self):
        self.assertOrgAndHtmlEqual('paragraph01.org', 'paragraph01.html')

    def test_table02(self):
        self.assertOrgAndHtmlEqual('table02.org', 'table02.html')

    def test_table03(self):
        self.assertOrgAndHtmlEqual('table03.org', 'table03.html')

    def test_text00(self):
        self.assertOrgAndHtmlEqual('text00.org', 'text00.html')


class TestShortcuts(unittest.TestCase):

    def test_html_shortcut(self):
        html = convert_html(load_data('table03.org'))
        expected = '\n'.join(load('table03.html'))
        self.assertEqual(html, expected)

    def test_html_with_highlight(self):
        html = convert_html(load_data('code01.org'), highlight=True)
        expected = '\n'.join(load('code01.html'))
        self.assertEqual(html, expected)

    def test_html_with_header_shortcut(self):
        html = convert_html(load_data('table03.org'), header=True)
        expected = '\n'.join(load('html_with_header.html'))
        self.assertEqual(html, expected)


class TestRst(unittest.TestCase):

    def assertOrgAndRstEqual(self, orgfile, rstfile):
        rst = convert(OrgDoc(load_data(orgfile)), 'rst')
        expected = load(rstfile)
        self.assertEqual(rst, expected)

    def test_code00(self):
        self.assertOrgAndRstEqual('code00.org', 'code00.rst')

    def test_definition00(self):
        self.assertOrgAndRstEqual('definition00.org', 'definition00.rst')

    def test_header00(self):
        rst = convert(OrgDoc(load_data('header00.org')), 'rst')
        expected = ['header1', '=======', '']
        self.assertEqual(rst, expected)

    def test_header01(self):
        self.assertOrgAndRstEqual('header01.org', 'header01.rst')

    def test_list00(self):
        self.assertOrgAndRstEqual('list00.org', 'list00.rst')

    def test_list01(self):
        self.assertOrgAndRstEqual('list01.org', 'list01.rst')

    def test_list02(self):
        self.assertOrgAndRstEqual('list02.org', 'list02.rst')

    def test_list03(self):
        self.assertOrgAndRstEqual('list03.org', 'list03.rst')

    def test_list05(self):
        self.assertOrgAndRstEqual('list05.org', 'list05.rst')

    def test_list06(self):
        self.assertOrgAndRstEqual('list06.org', 'list06.rst')

    def test_paragraph00(self):
        self.assertOrgAndRstEqual('paragraph00.org', 'paragraph00.rst')

    def test_paragraph01(self):
        self.assertOrgAndRstEqual('paragraph01.org', 'paragraph01.rst')

    def test_text00(self):
        self.assertOrgAndRstEqual('text00.org', 'text00.rst')


if __name__ == '__main__':
    unittest.main()