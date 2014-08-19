from Acquisition import aq_inner, aq_parent
#from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from yes.content.interfaces import IIssue

class IssueBannerViewlet(ViewletBase):
    
    def issue(self):
        issue = aq_parent(aq_inner(self.context))
        if IIssue.providedBy(issue):
            return issue
        
        # if not self.context.issue_topic:
        #     return None
        # 
        # catalog = getToolByName(aq_inner(self.context), 'portal_catalog')
        # res = catalog.searchResults(portal_type='Issue', issue_topic=self.context.issue_topic, sort_on='created', sort_order='descending', sort_limit=1)
        # if len(res):
        #     return res[0].getObject()
        # 
        # return None