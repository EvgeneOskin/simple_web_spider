print('Hello, my master!\n')

import argparse
parser = argparse.ArgumentParser(description='Process some web-operations',
                                 epilog='Bye.')
parser.add_argument('Where', action='store', nargs=1,
                    help='\"string\" link to web-site')
parser.add_argument('What', action='store', nargs=1,
                    help='\"string\" what to search')
parser.add_argument('--find', action='store_const', const = True,
                    default = False,
                    help='finding searched_for in searched_ling')
args = parser.parse_args()
in_data=vars(args)
print('You seaching ' + in_data['What'][0] + ' in ' + in_data['Where'][0])
print('I\'m quiting')
