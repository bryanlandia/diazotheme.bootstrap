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

    def _get_catalog_results(self, featured=False, limit=0):
        folder_path = '/'.join(self.context.getPhysicalPath())
        path_q = {'query': folder_path}
        types = ('Article', 'Blog Entry', )
        states = ('published', )
        sort = 'Date'
        
        results = self.catalog.searchResults(portal_types=types,
                                             path=path_q,
                                             review_state=states,
                                             is_featured=featured,
                                             sort_on=sort,  
                                             sort_order='descending',
                                             sort_limit=limit)

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

        mixed.append(featured.pop())
        mixed.append(featured.pop())
        mixed.append(featured.pop())

        while len(featured):    
            mixed.append(standard.pop())
            mixed.append(standard.pop())
            mixed.append(standard.pop())
            mixed.append(featured.pop())
        while len(standard):
            mixed.append(standard.pop())
        return list(mixed)

    def get_featured_listings(self, limit):
        return self._get_catalog_results(featured=True, limit=limit)

    def get_standard_listings(self, limit):
        return self._get_catalog_results(limit=limit)

    def __call__(self, limit):
        featured = self.get_featured_listings(limit)
        standard = self.get_standard_listings(limit)
        results = self._sort_to_features_mix(featured, standard)

        if results:
            contentlist = IContentListing(results)
            return contentlist
        else:
            return []
