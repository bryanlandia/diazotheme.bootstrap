from Acquisition import aq_inner, aq_parent
from zope.interface import implements
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from yes.diazotheme.browser.interfaces import ITopLevelTopicView

class TopLevelTopicView(BrowserView):
    """
    This is just a reuse of the normal Collection view, providing a special
    interface so that we can assign an extra viewlet to it. Misguided? Probably.
    """
    implements(ITopLevelTopicView)
    
    def __call__(self):
        return self.context.atct_topic_view.pt_render(extra_context={'view': self})

class SubtopicListing(ViewletBase):
    
    def topics(self):
        context = aq_inner(self.context)
        container = aq_parent(context)
        catalog = getToolByName(context, 'portal_catalog')
        atvm = getToolByName(context, 'portal_vocabularies')
        portal_url = getToolByName(context, 'portal_url')()

        # make sure we have a topic criterion
        query = self.context.buildQuery()
        if query is None:
            return []
        if 'category' not in query:
            return []
        
        # use the first top-level topic in the criterion
        subtopic_id = None
        top_level_topic_ids = dict([(t.UID(), t.getId()) for t in atvm.categories.contentValues()])
        for query_topic in query['category']['query']:
            if query_topic not in top_level_topic_ids:
                continue
            subtopic_id = top_level_topic_ids[query_topic]
        if subtopic_id is None:
            return
        
        # create map of topics for items in the current folder
        folder_topics = {}
        folder_items = catalog.searchResults(path='/'.join(container.getPhysicalPath()))
        for item in container.contentValues():
            category_field = item.getField('topic')
            if category_field is not None:
                category = category_field.getAccessor(item)()
                if category:
                    folder_topics[category] = item
            elif hasattr(item, 'buildQuery'):
                query = item.buildQuery()
                if query is not None and 'category' in query:
                    folder_topics[query['category']['query'][0]] = item

        # build list of topics with display info, based on order
        # from the ATVM
        subtopics = []
        for term in getattr(atvm.categories, subtopic_id).contentValues():
            id = term.getTermKey()
            title = term.getTermValue()
            try:
                item = folder_topics[id]
                url = item.absolute_url()
                description = item.Description()
            except KeyError:
                url = portal_url + '/search?category=%s' % id
                description = ''
            subtopics.append(dict(
                title=title,
                href=url,
                description=description,
            ))
        
        return subtopics
