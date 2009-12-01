
from zope.interface import implements

from plone.app.contentmenu import menu

class CombinedActionsWorkflowMenu( menu.ActionsMenu, menu.WorkflowMenu ):
    """ Combines the default actions- and the default workflow menu
    """
    implements( menu.IActionsMenu, menu.IWorkflowMenu )

    def getMenuItems( self, context, request ):
        # use default action menu items
        action_items = menu.ActionsMenu.getMenuItems(
                self, context, request
                )
        # use also default workflow menu items
        workflow_items = menu.WorkflowMenu.getMenuItems(
                self, context, request
                )
        if len( workflow_items )>0:
            workflow_items[0]['extra']['separator'] = 'actionSeparator'
        return action_items + workflow_items


class CombinedActionsWorkflowSubMenuItem( menu.ActionsSubMenuItem,
                                          menu.WorkflowSubMenuItem ):
    implements( menu.IActionsSubMenuItem, menu.IWorkflowSubMenuItem )

    def available( self ):
        if menu.ActionsSubMenuItem.available( self ):
            return True
        if menu.WorkflowSubMenuItem.available( self ):
            return True
        return False
