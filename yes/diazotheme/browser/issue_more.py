from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MoreFromIssueView(BrowserView):
    """ return a list of Articles from Issue which contains the context
        content item, or if not in an Issue, the current Issue.
    """

    index = ViewPageTemplateFile('issue_more.pt')

    def __init__(self, context, request):
        self.catalog = getToolByName(context, 'portal_catalog')
        self.context = context

    def _get_current_issue(self):
        return self.catalog.searchResults(portal_type='Issue',
                                          sort_on='issue_number',
                                          sort_limit=1,
                                          sort_order='reverse')[0].getObject()

    def issue(self):
        siteroot = getToolByName(self.context, 'portal_url').getPortalObject()
        item = self.context
        # traverse up the tree until we find an Issue or hit the site root
        while item.getParentNode() != siteroot:
            if item.portal_type == 'Issue':
                return item                
            item = item.getParentNode()
        # didn't find a containing Issue, so return the current Issue
        return self._get_current_issue()

    def articles(self):
        issue = self._get_issue()
        path_q = {'query': '/'.join(issue.getPhysicalPath())}
        articles = self.catalog.searchResults(portal_type='Article', 
                                              path=path_q, 
                                              sort_on='is_featured',
                                              sort_order='reverse',
                                              sort_limit=5,)
        return articles[:5]
