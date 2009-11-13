from zope.app.publisher.browser.menu import BrowserSubMenuItem
from zope.interface import implements
from plone.app.contentmenu.interfaces import IWorkflowSubMenuItem

class WorkflowSubMenuItem(BrowserSubMenuItem):
    """ a workflow menu that is always unavailable.
    """
    implements(IWorkflowSubMenuItem)

    def available(self):
        return False

