import argparse
import urllib2
import mimetools
import HTMLParser
            
class Content_parser(HTMLParser.HTMLParser):
    def __init__(self, in_data):
        HTMLParser.HTMLParser.__init__(self)
        self.data = in_data
  #  def handle_starttag(self, tag, attrs):
  #      try:
  #          print('tag: {0} with attributes {1}'.format(tag, attrs[0]))
  #      except:
  #          pass
    def handle_data(self, parsed_data):
        pasred_data = parsed_data.strip('\n')
        if self.data['What'] in pasred_data:
            print('find {0} in \n    {1}'.format(self.data['What'], parsed_data))

class connector:
    def __init__(self):
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
        self.data = vars(parser.parse_args())
        self.data['Where'] = self.data['Where'][0]
        self.data['What'] = self.data['What'][0]
        self.data['How_deep'] = self.data['How_deep'][0]
    def connect(self):
        try:
            self.Url_opened = urllib2.urlopen(self.data['Where'])
        except urllib2.URLError:
            print('Type a valid URL')
        else:
            print(self.Url_opened.info())
            content_url_L = self.Url_opened.readlines() 
            self.content_url_S = ''
            for S in content_url_L:
                self.content_url_S += S
            self.outfile = open('in.html', 'w')
            self.outfile.write(self.content_url_S)
            self.outfile.flush()
    def search(self):
        try:
            content_pasrer = Content_parser(in_data = self.data)
            content_pasrer.feed(self.content_url_S)
        except:
            print('Error in search')
        else:
            pass

