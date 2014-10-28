from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase


class IssueBannerViewlet(ViewletBase):
    
    def issue(self):
        catalog = getToolByName(aq_inner(self.context), 'portal_catalog')
        res = catalog.searchResults(portal_type='Issue', sort_on='created', 
                                    sort_order='descending', sort_limit=1)
        if len(res):
            return res[0].getObject()
        
        return None
