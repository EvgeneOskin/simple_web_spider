import connector
import unittest

class TestConnector(unittest.TestCase):
    
    def setUp(self):
        self.connector1 = connector.connector(in_arg = ['--find','file:///Users/eugen/projects/Web_spider/test/for_test.html','exemple','1'],
                                              DB_name = 'tested_DB.db')
        self.connector2 = connector.connector(in_arg = ['--find','file:///Users/eugen/projects/Web_spider/test/for_test.html','exempl1','1'],
                                              DB_name = 'tested_DB.db')
        self.tested_HTML = '''<html lang="en">
        <head>
        <title>exemple</title>
        </head>
        <body>
          <p>BlaBlaBla exemple
          another exemple</p>
        </body>
        </html>'''
        self.HTMLParser = connector.Content_parser(self.connector1.data, 'self')

    def test_deep_search1(self):
        self.assertTrue(self.connector1.deep_search())

    def test_deep_search2(self):
        self.assertTrue(not self.connector2.deep_search())

    def test_feeding(self):
        self.HTMLParser.feed(self.tested_HTML)
        self.assertEqual(self.HTMLParser.get_result(), 2)

suite = unittest.TestLoader().loadTestsFromTestCase(TestConnector)
unittest.TextTestRunner(verbosity=2).run(suite)
