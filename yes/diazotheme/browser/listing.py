from collections import deque

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.batching.batch import Batch

from plone.app.contentlisting.interfaces import IContentListing


class ArticlesListing(BrowserView):
    """ return a contentlisting of Articles (and for now, Blog Entries)
        contained within context and child objects
    """

    def __init__(self, context, request):
        self.catalog = getToolByName(context, 'portal_catalog')
        self.context = context
        self.qrymethod = self.catalog.searchResults

    def _get_catalog_results(self, featured=False, **kw):
        """ return catalog brains for published Articles and Blog Entries
            inside the context on which it's called
        """
        if 'context' in kw.keys():
            kw['path'] = {'query': '/'.join(kw['context'].getPhysicalPath())}

        types = ('Article', 'Blog Entry', )
        states = ('published', )
        sort = 'Date'
        
        results = self.qrymethod(portal_type=types,
                                 review_state=states,
                                 is_featured=featured,
                                 sort_on=sort,  
                                 sort_order='descending',
                                 **kw)

        return results

    def _sort_to_features_mix(self, featured, standard):
        """ Sort items thusly:
            3 from features list, add attr for Carousel
            3 from regular list
            1 from features list
            3 from regular list
            1 from features list
            ...
            and alternate 3 then 1 until there are no more features
            then just from regular list
        """

        mixed = deque()
        featured = deque(featured)
        standard = deque(standard)
        
        for i in range(1, 3):
            if len(featured):
                mixed.append(featured.pop())

        while len(featured):    
            mixed.append(standard.pop())
            mixed.append(standard.pop())
            mixed.append(standard.pop())
            mixed.append(featured.pop())
        while len(standard):
            mixed.append(standard.pop())
        return list(mixed)

    def get_featured_listings(self, **kw):
        return self._get_catalog_results(featured=True, **kw)

    def get_standard_listings(self, **kw):
        return self._get_catalog_results(featured=False, **kw)

    def __call__(self, batch=True, b_size=15, b_start=0, orphan=0, **kw):
        self.batch = batch
        self.b_size = b_size
        self.b_start = b_start
        self.orphan = orphan
        featured = self.get_featured_listings(**kw)
        standard = self.get_standard_listings(**kw)
        results = self._sort_to_features_mix(featured, standard)

        if results:
            # prune the results down to b_size 
            contentlist = IContentListing(results)
            if self.batch:
                batch = Batch(contentlist, b_size, b_start, orphan=3, 
                              pagerange=1)
                return batch

        else:
            return Batch([], 0)


class CollectionArticlesListing(ArticlesListing):

    def __init__(self, context, request):
        self.catalog = getToolByName(context, 'portal_catalog')
        self.context = context
        self.qrymethod = self._ATTopic_query

    def _ATTopic_query(self, **kw):
        """ pass parameters appropriately to ATTopic.queryCatalog method
            (REQUEST=None, batch=False, b_size=None,full_objects=False, **kw)
        """
        del kw['path']  # don't want to limit to context as w/ folders
        return self.context.queryCatalog(self.context.REQUEST, 
                                         False,  # no batch here
                                         None,  # no b_size here
                                         False,
                                         **kw)
