import unittest2 as unittest
from plone.app.contentmenu.interfaces import IActionsMenu, IFactoriesMenu
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFCore.utils import getToolByName
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.component import getUtility, provideAdapter
from zope.interface import Interface, alsoProvides, implements

from ftw.contentmenu.interfaces import IContentmenuPostFactoryMenu
from ftw.contentmenu.testing import FTW_CONTENTMENU_INTEGRATION_TESTING


class NullPostFactoryMenu(object):
    """This post factory menu adapter returns a empty list of factory,
    needed for testing purposes.
    """

    implements(IContentmenuPostFactoryMenu)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, factories):
        return []


class INullMarker(Interface):
    """Used to mark a context for using the null post factory menu.
    """


class TestActionsMenu(unittest.TestCase):

    layer = FTW_CONTENTMENU_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        wtool = getToolByName(self.portal, 'portal_workflow')
        wtool.setDefaultChain('simple_publication_workflow')

        # add fake action in the atfolder fti
        ttool = getToolByName(self.portal, 'portal_types')
        folder_fti = ttool.get('Folder')
        folder_fti.addAction(
            id='fake_action', name='Fake Action',
            action='string:${object_url}', condition='', permission=(),
            category='object_buttons', visible=True, icon_expr='', link_target='')

        self.folder = self.portal[self.portal.invokeFactory('Folder',
                                                            'folder')]
        self.folder.invokeFactory('Document', 'doc1')
        self.request = self.portal.REQUEST
        self.menu = getUtility(IBrowserMenu, name='ftw_contentmenu_actions',
                               context=self.folder)

    def test_actions_menu_interfaces(self):
        self.assertTrue(IBrowserMenu.providedBy(self.menu))
        self.assertTrue(IActionsMenu.providedBy(self.menu))

    def test_actions_menu_items(self):
        actions = self.menu.getActionsMenuItems(self.folder, self.request)
        action_ids = [a['extra']['id'] for a in actions]

        self.assertIn('copy', action_ids)
        self.assertTrue(len(action_ids) == len(set(action_ids)))

    def test_actionsmenu_items_from_typestool(self):
        # add a 'object_buttons' action to the 'Folder' fti
        types_tool = self.portal.portal_types
        fti = types_tool['Folder']
        fti.addAction('tt_test', 'Test Action', 'string:${object_url}', '',
                      '', 'object_buttons')
        actions = self.menu.getActionsMenuItems(self.folder, self.request)
        self.assertIn('tt_test', [a['extra']['id'] for a in actions])

    def test_workflow_menu_items(self):
        actions = self.menu.getWorkflowMenuItems(self.folder.doc1,
                                                 self.request)
        self.assertIn('workflow-transition-submit',
                      [a['extra']['id'] for a in actions])


class TestFactoriesMenu(unittest.TestCase):

    layer = FTW_CONTENTMENU_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        self.folder = self.portal[self.portal.invokeFactory('Folder',
                                                            'folder')]
        self.folder.invokeFactory('Document', 'doc1')
        self.request = self.portal.REQUEST
        self.menu = getUtility(IBrowserMenu, name='ftw_contentmenu_factory',
                               context=self.folder)

    def test_factories_menu_interfaces(self):
        self.assertTrue(IBrowserMenu.providedBy(self.menu))
        self.assertTrue(IFactoriesMenu.providedBy(self.menu))

    def test_menu_includes_factories(self):
        actions = self.menu.getMenuItems(self.folder, self.request)
        self.assertIn('image', [a['extra']['id'] for a in actions])

    def test_menu_includes_factory_actions(self):
        folder_fti = self.portal.portal_types['Folder']
        folder_fti.addAction('test_factory_action',
                             'Test Factory Action',
                             'string:${object_url}', '', '',
                             'folder_factories')
        actions = self.menu.getMenuItems(self.folder, self.request)
        self.assertIn('test_factory_action',
                      [a['extra']['id'] for a in actions])

        # test with permissions
        folder_fti.addAction('test_factory_action_perm',
                             'Test Factory Action',
                             'string:${object_url}', '', 'Add portal content',
                             'folder_factories')
        actions = self.menu.getMenuItems(self.folder, self.request)
        self.assertIn('test_factory_action_perm',
                      [a['extra']['id'] for a in actions])

    def test_post_menu_item_adapter(self):
        actions = self.menu.getMenuItems(self.folder, self.request)
        # we should have some actions
        self.assertTrue(len(actions) > 0)
        # register the null post factory menu adapter..
        provideAdapter(NullPostFactoryMenu,
                       (INullMarker, Interface),
                       IContentmenuPostFactoryMenu)
        alsoProvides(self.folder, INullMarker)
        # .. then we should not have any more actions
        actions = self.menu.getMenuItems(self.folder, self.request)
        self.assertEqual(len(actions), 0)

    def test_menu_of_default_page_includes_factory_actions(self):
        folder_fti = self.portal.portal_types['Folder']
        folder_fti.addAction('test_factory_action',
                             'Test Factory Action',
                             'string:${object_url}', '', '',
                             'folder_factories')
        self.folder.default_page = 'doc1'
        actions = self.menu.getMenuItems(self.folder.doc1, self.request)
        self.assertIn('test_factory_action',
                      [a['extra']['id'] for a in actions])
