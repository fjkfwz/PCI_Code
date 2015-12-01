import searchengine
pagelist = ['http://wiki.openwrt.org/zh-cn/doc/howto/obtain.firmware.generate']
# searchengine.crawler('searchindex.db').createindextables()
# searchengine.crawler('searchindex.db').crawl(pagelist)
searchengine.search('searchindex.db').query('html n')
# searchengine.crawler('searchindex.db').caculatepagerank()