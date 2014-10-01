from collections import deque

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from plone.app.contentlisting.interfaces import IContentListing


class ArticlesListing(BrowserView):
    """ return a contentlisting of Articles (and for now, Blog Entries)
        contained within context and child objects
    """

    def __init__(self, context, request):
        self.catalog = getToolByName(context, 'portal_catalog')
        self.context = context

    def _get_catalog_results(self, featured=False, limit=0, **kw):
        """ return catalog brains for published Articles and Blog Entries
            inside the context on which it's called
        """
        if kw['context']:
            kw['path'] = {'query': '/'.join(kw['context'].getPhysicalPath())}

        types = ('Article', 'Blog Entry', )
        states = ('published', )
        sort = 'Date'
        
        results = self.catalog.searchResults(portal_type=types,
                                             review_state=states,
                                             is_featured=featured,
                                             sort_on=sort,  
                                             sort_order='descending',
                                             sort_limit=limit,
                                             **kw)

        return results[:limit]

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

    def get_featured_listings(self, limit, **kw):
        return self._get_catalog_results(featured=True, limit=limit, **kw)

    def get_standard_listings(self, limit, **kw):
        return self._get_catalog_results(featured=False, limit=limit, **kw)

    def __call__(self, limit, **kw):
        featured = self.get_featured_listings(limit, **kw)
        standard = self.get_standard_listings(limit, **kw)
        results = self._sort_to_features_mix(featured, standard)[:limit]

        if results:
            contentlist = IContentListing(results)
            return contentlist
        else:
            return []
