from Acquisition import aq_inner
from Products.CMFCore.interfaces import IActionProvider
from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFPlone import PloneMessageFactory as _
from ftw.contentmenu.interfaces import IContentmenuPostFactoryMenu
from plone.app.contentmenu import menu
from plone.app.contentmenu.interfaces import IFactoriesSubMenuItem
from plone.app.contentmenu.interfaces import IWorkflowSubMenuItem
from zope.component import queryMultiAdapter, getMultiAdapter
from zope.i18n import translate
from zope.interface import implements


class CombinedActionsWorkflowMenu(menu.ActionsMenu, menu.WorkflowMenu):
    """ Combines the default actions- and the default workflow menu
    """
    implements(menu.IActionsMenu, menu.IWorkflowMenu)

    def getMenuItems(self, context, request):
        # action menu items
        action_items = self.getActionsMenuItems(
            context, request
            )

        # workflow menu items
        workflow_items = self.getWorkflowMenuItems(
            context, request
            )
        if len(workflow_items) > 0:
            workflow_items[0]['extra']['separator'] = 'actionSeparator'

        return action_items + workflow_items

    def getActionsMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        context_state = getMultiAdapter((context, request),
            name='plone_context_state')
        edit_actions = context_state.actions('object_buttons')

        if not edit_actions:
            return results

        actionicons = getToolByName(context, 'portal_actionicons')
        portal_url = getToolByName(context, 'portal_url')()

        for action in edit_actions:
            if action['allowed']:
                aid = action['id']
                cssClass = 'actionicon-object_buttons-%s' % aid
                icon = action.get('icon', None)
                if not icon:
                    # allow fallback to action icons tool
                    icon = actionicons.queryActionIcon('object_buttons', aid)
                    if icon:
                        icon = '%s/%s' % (portal_url, icon)

                results.append({
                        'title': action['title'],
                        'description': '',
                        'action': action['url'],
                        'selected': False,
                        'icon': icon,
                        'extra': {'id': aid,
                                  'separator': None,
                                  'class': cssClass},
                        'submenu': None, })

        results.sort(key=lambda x: translate(x['title'], context=request))
        return results

    # workflow menu items
    # 'policy...' item is only visible for managers
    def getWorkflowMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []
        context = aq_inner(context)

        wf_tool = getToolByName(context, 'portal_workflow')
        workflowActions = wf_tool.listActionInfos(object=context)

        locking_info = queryMultiAdapter((context, request),
                                         name='plone_lock_info')
        if locking_info and locking_info.is_locked_for_current_user():
            return []

        for action in workflowActions:
            if action['category'] != 'workflow':
                continue

            cssClass = 'kssIgnore'
            actionUrl = action['url']
            if actionUrl == "":
                actionUrl = '%s/content_status_modify?workflow_action=%s' % (
                    context.absolute_url(),
                    action['id'])
                cssClass = ''

            description = ''

            transition = action.get('transition', None)
            if transition is not None:
                description = transition.description

            for bogus in self.BOGUS_WORKFLOW_ACTIONS:
                if actionUrl.endswith(bogus):
                    if getattr(context, bogus, None) is None:
                        actionUrl = context.absolute_url() + \
                            '/content_status_modify?workflow_action=' + \
                            action['id']
                        cssClass = ''
                    break

            if action['allowed']:
                results.append({
                        'title': action['title'],
                        'description': description,
                        'action': actionUrl,
                        'selected': False,
                        'icon': None,
                        'extra': {'id': 'workflow-transition-' +
                                      action['id'],
                                  'separator': None,
                                  'class': cssClass},
                        'submenu': None,
                        })

        url = context.absolute_url()

        if len(results) > 0:
            results.append({
                    'title': _(u'label_advanced', default=u'Advanced...'),
                    'description': '',
                    'action': url + '/content_status_history',
                    'selected': False,
                    'icon': None,
                    'extra': {'id': 'advanced',
                              'separator': 'actionSeparator',
                              'class': 'kssIgnore'},
                    'submenu': None,
                             })

        if getToolByName(
            context, 'portal_placeful_workflow', None) is not None \
                and _checkPermission('Manage portal', context):
            results.append({
                    'title': _(u'workflow_policy', default=u'Policy...'),
                    'description': '',
                    'action': url + '/placeful_workflow_configuration',
                    'selected': False,
                    'icon': None,
                    'extra': {'id': 'policy',
                                     'separator': None,
                                     'class': 'kssIgnore'},
                    'submenu': None,
                             })

        return results


class CombinedActionsWorkflowSubMenuItem(menu.ActionsSubMenuItem,
                                         menu.WorkflowSubMenuItem):
    """The menu item linking to the actions menu."""

    implements(menu.IActionsSubMenuItem, menu.IWorkflowSubMenuItem)
    submenuId = 'ftw_contentmenu_actions'

    def available(self):
        actions_tool = getToolByName(self.context, 'portal_actions')
        edit_actions = actions_tool.listActionInfos(object=self.context,
            categories=('object_buttons',), max=1)
        if len(edit_actions) > 0:
            return True

        provider = getattr(actions_tool, 'portal_types', None)
        if IActionProvider.providedBy(provider):
            type_actions = provider.listActionInfos(object=self.context,
                category='object_buttons', max=1)
            if len(type_actions) > 0:
                return True

        context_state = getMultiAdapter((self.context, self.request),
                                        name='plone_context_state')
        if context_state.workflow_state() is not None:
            return True
        return False


class FactoriesSubMenuItem(menu.FactoriesSubMenuItem):
    """The menu item linking to the factories menu."""

    implements(IFactoriesSubMenuItem)
    submenuId = 'ftw_contentmenu_factory'

    def available(self):
        if self._addingToParent() and not self.context_state.is_default_page():
            return False
        if len(self._itemsToAdd()) > 0:
            return True
        if self._showConstrainOptions():
            return True

        actions_tool = getToolByName(self.context, 'portal_actions')
        provider = getattr(actions_tool, 'portal_types', None)
        if IActionProvider.providedBy(provider):
            type_actions = provider.listActionInfos(object=self.context,
                           category='folder_factories', max=1)
            if len(type_actions) > 0:
                return True

        return False


class FactoriesMenu(menu.FactoriesMenu):
    """ Extends the plone FactoriesMenu
    """

    def getMenuItems(self, context, request):
        # get standard factory types
        factories = super(FactoriesMenu, self).getMenuItems(context, request)

        # get factory actions from 'portal_types' action provider
        type_actions = []
        actions_tool = getToolByName(aq_inner(context), 'portal_actions')
        provider = getattr(actions_tool, 'portal_types', None)
        if IActionProvider.providedBy(provider):
            type_actions = provider.listActionInfos(object=context,
                           category='folder_factories')

        if type_actions:
            # WARNING: use of portal_actionicons is deprecated!
            plone_utils = getToolByName(context, 'plone_utils')
            portal_state = getMultiAdapter((context, request),
                                           name='plone_portal_state')
            portal_url = portal_state.portal_url()

            for action in type_actions:
                if action['allowed']:
                    cssClass = 'actionicon-folder_factories-%s' % action['id']
                    icon = action['icon']
                    if not icon:
                        icon = plone_utils.getIconFor('folder_factories',
                                                      action['id'],
                                                      None)
                        if icon:
                            icon = '%s/%s' % (portal_url, icon)

                    factories.append({
                            'title': action['title'],
                            'description': '',
                            'action': action['url'],
                            'selected': False,
                            'icon': icon,
                            'extra': {'id': action['id'],
                                             'separator': None,
                                             'class': cssClass},
                            'submenu': None,
                           })

        # order the actions
        factories.sort(key=lambda x: translate(x.get('title', u''),
                                               domain='plone',
                                               context=request))

        return self._post_cleanup_factories(context, request, factories)

    def _post_cleanup_factories(self, context, request, factories):
        """For easier hook-in we call the IContentmenuPostFactoryMenu adapter,
        which may clean up the factories list.
        """

        adpt = queryMultiAdapter((context, request),
                                 IContentmenuPostFactoryMenu)

        if adpt:
            return adpt(factories)
        else:
            return factories


class WorkflowSubMenuItem(menu.WorkflowSubMenuItem):
    """A workflow menu that is always unavailable.
    """
    implements(IWorkflowSubMenuItem)

    def available(self):
        return False
