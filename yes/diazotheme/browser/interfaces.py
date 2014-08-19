from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from plone.app.portlets.interfaces import IColumn


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "YES! Magazine theme" theme, this interface must be its layer
       (in plonetheme/viewlets/configure.zcml).
    """


class ITopLevelTopicView(Interface):
    """
    Marker for a collection view used for a top-level topic of the taxonomy.
    """


class ITopCenterPortlets(IColumn):
    """portlet manager for content column header portlets"""


class IAboveContentTitlePortlets(IColumn):
    """portlet manager for portlets above the content title"""