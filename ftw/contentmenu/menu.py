from Acquisition import aq_inner
from plone.app.contentmenu import menu
from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFPlone import PloneMessageFactory as _
from zope.component import queryMultiAdapter
from zope.interface import implements


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
        workflow_items = self.getWorkflowMenuItems(
                context, request
                )
        if len( workflow_items )>0:
            workflow_items[0]['extra']['separator'] = 'actionSeparator'
        return action_items + workflow_items

    # workflow menu items
    # 'advanced...' and 'policy...' items are only visible for managers
    def getWorkflowMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []
        context = aq_inner(context)

        wf_tool = getToolByName(context, 'portal_workflow')
        workflowActions = wf_tool.listActionInfos(object=context)

        locking_info = queryMultiAdapter((context, request), name='plone_lock_info')
        if locking_info and locking_info.is_locked_for_current_user():
            return []

        for action in workflowActions:
            if action['category'] != 'workflow':
                continue

            cssClass = 'kssIgnore'
            actionUrl = action['url']
            if actionUrl == "":
                actionUrl = '%s/content_status_modify?workflow_action=%s' % (context.absolute_url(), action['id'])
                cssClass = ''

            description = ''

            transition = action.get('transition', None)
            if transition is not None:
                description = transition.description

            for bogus in self.BOGUS_WORKFLOW_ACTIONS:
                if actionUrl.endswith(bogus):
                    if getattr(context, bogus, None) is None:
                        actionUrl = '%s/content_status_modify?workflow_action=%s' % (context.absolute_url(), action['id'],)
                        cssClass =''
                    break

            if action['allowed']:
                results.append({ 'title'       : action['title'],
                                 'description' : description,
                                 'action'      : actionUrl,
                                 'selected'    : False,
                                 'icon'        : None,
                                 'extra'       : {'id': 'workflow-transition-%s' % action['id'], 'separator': None, 'class': cssClass},
                                 'submenu'     : None,
                                 })

        url = context.absolute_url()

        if len(results) > 0 and _checkPermission('Manage portal', context):
            results.append({ 'title'        : _(u'label_advanced', default=u'Advanced...'),
                             'description'  : '',
                             'action'       : url + '/content_status_history',
                             'selected'     : False,
                             'icon'         : None,
                             'extra'        : {'id': 'advanced', 'separator': 'actionSeparator', 'class': 'kssIgnore'},
                             'submenu'      : None,
                            })

        if getToolByName(context, 'portal_placeful_workflow', None) is not None\
           and _checkPermission('Manage portal', context):
            results.append({ 'title'       : _(u'workflow_policy', default=u'Policy...'),
                             'description' : '',
                             'action'      : url + '/placeful_workflow_configuration',
                             'selected'    : False,
                             'icon'        : None,
                             'extra'       : {'id': 'policy', 'separator': None, 'class': 'kssIgnore'},
                             'submenu'     : None,
                            })

        return results

class CombinedActionsWorkflowSubMenuItem( menu.ActionsSubMenuItem,
                                          menu.WorkflowSubMenuItem ):
    implements( menu.IActionsSubMenuItem, menu.IWorkflowSubMenuItem )

    def available( self ):
        if menu.ActionsSubMenuItem.available( self ):
            return True
        if menu.WorkflowSubMenuItem.available( self ):
            return True
        return False
