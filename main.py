print('Hello, my master!\n')

import connector

spider=connector.connector()
info_msg = 'You seaching \"{0}\" in {1} in deep level {2}'.format(
    spider.data['What'], spider.data['Where'].keys()[0], spider.data['How_deep'])
print(info_msg)
spider.deep_search()
print('I\'m quiting')
