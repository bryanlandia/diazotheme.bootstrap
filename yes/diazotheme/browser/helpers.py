import re
from time import time
from lxml import html

import requests

from Products.Five import BrowserView
from plone.memoize import ram


class GooglePlusGetter(BrowserView):
    """ Use this intermediary for GooglePlus requests since they don't allow
        cross-domain requests from JavaScript. Note these may stop working, but
        as these counts aren't available through their api and are discouraged,
        this is the only way unless we use their widgets.
    """

    GPLUS_URL = "https://plusone.google.com/_/+1/fastbutton?url=%s&callback=?"
    shares_match = re.compile("window\.__SSR = {c: ([\d]+)")
    plusones_match = "//*[@id='aggregateCount']"

    def gplus_resp_cache_key(self, func, request):
        return "%s%s%s" % (func.__repr__(), 
                           time() // (60 * 5), request.get('page_url'))

    @ram.cache(gplus_resp_cache_key)
    def get_gplus_resp(self, request):
        page_url = request.get('page_url')
        url = self.GPLUS_URL % page_url
        resp = requests.get(url)
        return resp._content

    def shares_cache_key(self, func):
        return "%s%s%s" % (func.__repr__(), 
                           time() // (60 * 5), self.request.get('page_url'))

    # @ram.cache(shares_cache_key)
    def get_shares(self):  
        request = self.request
        resp = self.get_gplus_resp(request)       
        try:
            count = re.search(self.shares_match, resp).group(1)
            return count
        except:
            return ''

    def plusones_cache_key(self, func):
        return "%s%s%s" % (func.__repr__(), 
                           time() // (60 * 5))

    # @ram.cache(plusones_cache_key)
    def get_plusones(self):
        request = self.request
        resp = self.get_gplus_resp(request)
        try:
            tree = html.fromstring(resp)
            count = tree.xpath('//*[@id="aggregateCount"]/text()')[0]
            return count
        except:
            return ''            
