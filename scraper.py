from gevent import monkey
monkey.patch_all()

from datetime import datetime
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
req = 1
pool = gevent.pool.Pool(32)
queue = gevent.queue.Queue()


def parse_mobile(params):
    global mobiles,errors,req

    url = params['url']
    comp_name = params['name']

    print 'Request sent for - ' + url
    req += 1
    try:
        mobiles += 1
        tree = html.fromstring(session.get(url).text)
        name = tree.xpath('//h1[@class="specs-phone-name-title"]//text()')[0]
        print 'Mobile found : ',name
        data[comp_name][name] = {}
        data[comp_name][name]['url'] = url
        func = lambda x: data[comp_name][name].update({x.xpath('.//td[@class="ttl"]/a/text()')[0]:x.xpath('.//td[@class="nfo"]/text()')})
        [ func(x) for x in tree.xpath('//div[@id="specs-list"]//table//tr') if x.xpath('.//td[@class="ttl"]/a/text()') != []]

    except Exception as e:
        print 'Error in %s Restarting.... \n Error message : %s' % (url,e.message)
        queue.put_nowait((parse_mobile,params))
        errors += 1

def parse_comp(params):
    global errors,req

    url = params['url']
    comp_name = params['name']
    data[comp_name] = {}

    dp.append(url)
    print 'Request sent for [%s] - %s' % (comp_name,url)
    req += 1
    try:
        tree = html.fromstring(session.get(url).text)
        [ queue.put_nowait(( parse_comp,{'url':domain+x,'name':comp_name} )) for x in tree.xpath('//div[@class="nav-pages"]//a/@href') if domain+x not in dp ]
        [ queue.put_nowait(( parse_mobile,{'url':domain+x,'name':comp_name} )) for x in tree.xpath('//div[@class="makers"]//a/@href') ]
    except Exception as e:
        print 'Error in %s Restarting.... \n Error message : %s' % (url,e.message)
        queue.put_nowait((parse_comp,params))
        errors += 1

def scrape_base_url():
    startTime = datetime.now()
    tree = html.fromstring(session.get(base_url).text)

    # [ queue.put_nowait((parse_comp,{'url':domain+x.xpath('./a/@href')[0],'name':x.xpath('./a/text()')[0] } )) for x in tree.xpath('//div[@class="st-text"]//td') if x.xpath('./a/text()')!=[] ]

    func = lambda x: queue.put_nowait((parse_comp,{'url':domain+x.xpath('./a/@href')[0],'name':x.xpath('./a/text()')[0] } ))
    [ func(x) for x in tree.xpath('//div[@class="st-text"]//td') if x.xpath('./a/text()')!=[] ]


    while not queue.empty() and not pool.full():
        for x in xrange(0, min(queue.qsize(), pool.free_count())):
            t = queue.get_nowait()
            pool.start(pool.spawn(t[0],t[1]))
    pool.join()
    print 'Time Taken : ',datetime.now() - startTime

if __name__ == '__main__':
    scrape_base_url()
    print 'No of mobiles stored : ',mobiles
    print 'No of requests made : ',req
    print 'No of errors : ',errors
