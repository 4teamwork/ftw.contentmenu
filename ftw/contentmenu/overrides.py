from zope.app.publisher.browser.menu import BrowserSubMenuItem
from plone.app.contentmenu import menu  
from zope.interface import implements
from plone.app.contentmenu.interfaces import IWorkflowSubMenuItem

class WorkflowSubMenuItem(menu.WorkflowSubMenuItem):
    """ a workflow menu that is always unavailable.
    """
    implements(IWorkflowSubMenuItem)

    def available(self):
        if self.context.portal_type != 'opengever.document.document':
            return False
        return super(WorkflowSubMenuItem, self).available()
