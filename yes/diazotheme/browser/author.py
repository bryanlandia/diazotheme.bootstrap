from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


class AuthorView(BrowserView):
    """BV to list content created by this author. Note we're using a custom
    index for author
    """
    
    def __init__(self, context, request):
        super(AuthorView, self).__init__(context, request)
        self.author = self.request.get('author', None)
    
    def getAuthor(self):
        return self.author
    
    def getContent(self):
        """Return catalog brains for content by this author.
        Don't specify portal_type, but let the scope of the creators index
        dictate.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(creators = self.author,
                       sort_on = 'effective',
                       sort_order = 'reverse',
                       )
    