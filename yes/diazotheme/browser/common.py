from plone.app.layout.links.viewlets import RSSViewlet as base_RSSViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.googleanalytics.viewlets.tracking import \
    AnalyticsTrackingViewlet as base_ga_tracking_viewlet


class AnalyticsTrackingViewlet(base_ga_tracking_viewlet):
    render = ViewPageTemplateFile('tracking.pt')


class RSSViewlet(base_RSSViewlet):
    index = ViewPageTemplateFile('rsslink.pt')