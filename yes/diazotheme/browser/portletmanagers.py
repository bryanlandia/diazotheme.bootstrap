from zope.interface import Interface
from zope.component import adapts
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.manager import (
    ColumnPortletManagerRenderer as BaseColumnPortletManagerRenderer)
from Products.CMFCore.utils import getToolByName
from plone.portlets.interfaces import ILocalPortletAssignable

from yes.diazotheme.browser.interfaces import ITopCenterPortlets
from yes.diazotheme.browser.interfaces import IAboveContentTitlePortlets

import logging


logger = logging.getLogger('portlets')


class TopCenterPortletManagerRenderer(BaseColumnPortletManagerRenderer):
    """A renderer for top center portlets.
    """
    adapts(Interface, IDefaultBrowserLayer, IBrowserView,
           ITopCenterPortlets)
    template = ViewPageTemplateFile('renderer-top-center.pt')


    def base_url(self):
        """Return URL of context regardless of whether it is a default page.
        """
        return self.context.absolute_url()

    def can_manage_portlets(self):
        context = self.context
        if not ILocalPortletAssignable.providedBy(context):
            return False
        mtool = getToolByName(context, 'portal_membership')
        return mtool.checkPermission("Portlets: Manage portlets", context)


class AboveContentTitlePortletManagerRenderer(TopCenterPortletManagerRenderer):
    """ A renderer for portlets above the content title 
    """
    adapts(Interface, IDefaultBrowserLayer, IBrowserView,
           IAboveContentTitlePortlets)
    template = ViewPageTemplateFile('renderer-above-content-title.pt')            