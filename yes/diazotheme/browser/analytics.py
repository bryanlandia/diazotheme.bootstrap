from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.googleanalytics.tracking.plugins import \
    AnalyticsCommentPlugin as base_AnalyticsCommentPlugin


class AnalyticsCommentPlugin(base_AnalyticsCommentPlugin):
    """
    A tracking plugin to track posting of comments.
    Override to use our own comments.pt
    """
    # was unable to override using z3c.jbot template BW

    __call__ = ViewPageTemplateFile('ga_comment_plugin.pt')