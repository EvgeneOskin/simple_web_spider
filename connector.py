import argparse
import urllib2
import mimetools
import HTMLParser
import urlparse
import sqlite3

class Content_parser(HTMLParser.HTMLParser):
    def __init__(self, in_data, URL):
        HTMLParser.HTMLParser.__init__(self)
        self.data = in_data
        self.currentURL = URL
        self.links = {}
        self.times_matched = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attrs_iter in attrs:
                if attrs_iter[0] == 'href':
                    new_URL = urlparse.urljoin(self.currentURL, attrs_iter[1])
                    if not new_URL in self.data['Where']:
                        self.links[new_URL] = False
            
    def handle_data(self, parsed_data):
        pasred_data = parsed_data.strip('\n')
        if self.data['What'] in pasred_data:
            self.times_matched += 1
            print('find: "{0}"\nin "{1}"'.format(self.data['What'], self.currentURL))
            
    def get_links(self):
        return self.links
        
    def get_result(self):
        return self.times_matched
    
class connector:
    def __init__(self, in_arg = None, DB_name = 'search_result.db'):
        parser = argparse.ArgumentParser(description='Process some web-operations',
                                         epilog='Bye.')
        parser.add_argument('Where', action='store', nargs=1,
                            help='\"string\" link to \"home\"-web-site')
        parser.add_argument('What', action='store', nargs=1,
                            help='\"string\" what to search')
        parser.add_argument('How_deep', action='store', nargs=1, type=int,
                            help='''\"int\" how deep in \"home\"-web-site
                            it need to be searched''')
        parser.add_argument('--find', action='store_const', const = True, default = False,
                            help='finding searched_for in searched_ling')
        self.data = vars(parser.parse_args(in_arg))
        self.data['Where'] = {self.data['Where'][0]: False}
        self.data['What'] = self.data['What'][0]
        self.data['How_deep'] = self.data['How_deep'][0]
        self.search_result = False
        self.new_data_where = {}
        self.sqlite3_DB = sqlite3.connect(DB_name)
        self.DB_cursor = self.sqlite3_DB.cursor()
        try:
            self.DB_cursor.execute('CREATE TABLE result(lines INT, what TEXT, links TEXT)')
        except:
            pass

    def connect(self):
        URLlist = self.data['Where'].keys()
        for current_URL in URLlist:
            if not self.data['Where'][current_URL]:
                self.data['Where'][current_URL] = True
                try:
                    self.Url_opened = urllib2.urlopen(current_URL)
                except urllib2.URLError:
                    print('Type a valid URL ' + current_URL)
                    try:
                        NNS=input('PRESS')
                    except:
                        pass
                else:
                    content_url_L = self.Url_opened.readlines() 
                    self.content_url_S = ''
                    for S in content_url_L:
                        self.content_url_S += S
                    self.search(current_URL)

    def search(self, current_URL):
        searcher = Content_parser(in_data = self.data, URL = current_URL)
        try:
            searcher.feed(self.content_url_S)
        except HTMLParser.HTMLParseError:
            print('Here I have HTMLParseError: {0}'.format(current_URL))
        else:
            current_result = searcher.get_result()
            if current_result == 0:
                needed_links = searcher.get_links()
                self.new_data_where.update(needed_links)
            else:
                self.search_result = True
                self.DB_cursor.execute(
                    'INSERT INTO result VALUES(?,?,?)',
                    (current_result, self.data['What'], current_URL))
                self.sqlite3_DB.commit()
            return current_result
                
    def deep_search(self):
        self.current_deeps = 0
        while not self.search_result and self.current_deeps != self.data['How_deep']:
            self.connect()
            self.current_deeps += 1
            self.data['Where'].update(self.new_data_where)
            self.new_data_where.clear()
        self.DB_cursor.close()
        if self.search_result:
            print ('ALL OK, I FIND IT')
            return True
        print ('Please search in anouther web_site or type anouther key-word')
        return False
