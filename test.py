from gevent import monkey
monkey.patch_all()

from lxml import html
import requests
import gevent.pool
import gevent.queue

domain = 'http://www.gsmarena.com/'
base_url = 'http://www.gsmarena.com/makers.php3'
session = requests.Session()
dp = []
data = {}
mobiles = 0
errors = 0
req = 0
pool = gevent.pool.Pool(32)
queue = gevent.queue.Queue()

from datetime import datetime
startTime = datetime.now()

def parse_mobile(url):
    global mobiles,errors,req
    mobiles += 1
    print 'Request sent for - ' + url
    req += 1
    try:
        tree = html.fromstring(session.get(url).text)
        name = tree.xpath('//h1[@class="specs-phone-name-title"]//text()')[0]
        print 'Mobile found : ',name
        data[name] = {'url':url}
    except Exception as e:
        print 'Error in ',url,'Restarting.... \n Error message : ',e.message
        # queue.put_nowait((parse_mobile,url))
        errors += 1

def parse_comp(url):
    global errors,req
    dp.append(url)
    print 'Request sent for - ' + url
    req += 1
    try:
        tree = html.fromstring(session.get(url).text)
        [ queue.put_nowait((parse_comp,(domain+x))) for x in tree.xpath('//div[@class="nav-pages"]//a/@href') if domain+x not in dp ]
        [ queue.put_nowait((parse_mobile,(domain+x))) for x in tree.xpath('//div[@class="makers"]//a/@href') ]
    except Exception as e:
        print 'Error in ',url,'Restarting.... \n Error message : ',e.message
        # queue.put_nowait((parse_comp,url))
        errors += 1

def scrape_base_url():
    tree = html.fromstring(session.get(base_url).text)
    [ queue.put_nowait((parse_comp,(domain+x.xpath('./a/@href')[0]))) for x in tree.xpath('//div[@class="st-text"]//td') if x.xpath('./a/text()')!=[] ]

    while not queue.empty() and not pool.full():
        for x in xrange(0, min(queue.qsize(), pool.free_count())):
            t = queue.get_nowait()
            pool.start(pool.spawn(t[0],t[1]))
    pool.join()

if __name__ == '__main__':
    scrape_base_url()
    print 'No of mobiles stored : ',mobiles
    print 'No of requests made : ',req+1
    print 'No of errors : ',errors
    print 'Time Taken : ',datetime.now() - startTime

'''
Time Taken :  0:08:27.941211
No of mobiles stored :  8026
No of requests made :  8274
No of errors :  286
Ram used : 2.8 GB
'''
