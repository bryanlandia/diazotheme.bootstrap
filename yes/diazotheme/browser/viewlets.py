from cgi import escape

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.utils import safe_unicode
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import common as base

from quintagroup.seoptimizer.browser.viewlets import TitleCommentNoframeViewlet
from quintagroup.canonicalpath.interfaces import ICanonicalLink

from yes.content.config import TOP_LEVEL_TOPIC_SECTIONS


class GlobalSectionsViewlet(base.GlobalSectionsViewlet):
	"""just needed an extra wrapper div"""
	index = ViewPageTemplateFile('sections.pt')

    
class YESTitleCommentNoframeViewlet(TitleCommentNoframeViewlet):
    """ quintagroup.seoptimizer html title viewlet which also uses author
        name for the standard title (no seo title override)
    """
    
    def render(self):
        portal_title = safe_unicode(self.portal_state.portal_title())
        if self.override_title:
            qseo_title = u"<title>%s &mdash; %s</title>" % (
                escape(safe_unicode(self.seo_context["seo_title"])), 
                escape(safe_unicode(portal_title))
                )
        else:
            qseo_title = self.std_title()

        comments = ""
        if self.has_comments:
            comments = u"\n<!--%s-->" % escape(safe_unicode(
                self.seo_context["seo_html_comment"]))

        if self.has_noframes:
            noframes = u"<noframes>%s</noframes>" % escape(safe_unicode(
                self.seo_context["seo_noframes"]))
        else:
            noframes = ""

        return qseo_title + comments + noframes        

    def std_title(self):
        page_title = safe_unicode(self.context_state.object_title())
        portal_title = safe_unicode(self.portal_state.portal_title())
        if page_title == portal_title:
            return u"<title>%s</title>" % (escape(portal_title))
        else:
            authtext = self.authorText()
            return u"<title>%s %s &mdash; %s</title>" % (
                escape(safe_unicode(page_title)),
                escape(safe_unicode(authtext)),
                escape(safe_unicode(portal_title)))

    def authorText(self):
        """ get author(s) name for use in HTML title.  We only use capitalized
        names from creator field.
        """    
        creators = [c for c in self.context.listCreators() if c and \
            ord('a') > ord(c[0])]
        if len(creators) == 0:
            authtext =  ""
        elif len(creators) == 1:
            authtext = "by %s" % creators[0]
        else:
            authtext = "by " + ", ".join(creators[:-1]) + " and %s" % creators[-1]
        return escape(safe_unicode(authtext))
     
        
class DisqusJSHeadViewlet(base.ViewletBase):
    
    def getCanonicalLink(self):
        return ICanonicalLink(self.context).getProp()


class TopicSectionViewlet(base.ViewletBase):

    index = ViewPageTemplateFile('topic_section.pt')

    def topicSection(self):
        path = self.context.getPhysicalPath()
        ptool = getToolByName(self.context, 'portal_url')
        siterootpath = ptool.getPortalObject().getPhysicalPath()
        toplevelpath = path[len(siterootpath)]
        if toplevelpath in TOP_LEVEL_TOPIC_SECTIONS:
            return toplevelpath
        else:
            return None



