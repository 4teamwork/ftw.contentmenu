from Products.PloneTestCase.ptc import PloneTestCase
from ftw.contentmenu.interfaces import IContentmenuPostFactoryMenu
from ftw.contentmenu.tests.layer import Layer
from plone.app.contentmenu.interfaces import IActionsMenu, IFactoriesMenu
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.component import getUtility, provideAdapter, queryMultiAdapter
from zope.interface import Interface, alsoProvides, implements
from zope.interface import noLongerProvides

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


class TestActionsMenu(PloneTestCase):

    layer = Layer

    def afterSetUp(self):
        self.folder.invokeFactory('Document', 'doc1')
        self.menu = getUtility(IBrowserMenu, name='ftw_contentmenu_actions',
                               context=self.folder)
        self.request = self.app.REQUEST
        # add a 'object_buttons' action to the 'Folder' fti
        types_tool = self.portal.portal_types
        fti = types_tool['Folder']
        fti.addAction('tt_test', 'Test Action', 'string:${object_url}' ,'',
                      '', 'object_buttons')

    def test_ActionsMenuImplementsIBrowserMenu(self):
        self.failUnless(IBrowserMenu.providedBy(self.menu))

    def test_ActionsMenuImplementsIActionsMenu(self):
        self.failUnless(IActionsMenu.providedBy(self.menu))

    def test_actions_menu_items(self):
        actions = self.menu.getActionsMenuItems(self.folder, self.request)
        self.failUnless('copy' in [a['extra']['id'] for a in actions])

    def test_actionsmenu_items_from_typestool(self):
        actions = self.menu.getActionsMenuItems(self.folder, self.request)
        self.failUnless('tt_test' in [a['extra']['id'] for a in actions])

    def test_worklfow_menu_items(self):
        actions = self.menu.getWorkflowMenuItems(self.folder.doc1,
                                                 self.request)
        self.failUnless('workflow-transition-submit' in
                        [a['extra']['id'] for a in actions])

    def test_workflowmenu_items_advanced(self):
        actions = self.menu.getWorkflowMenuItems(self.folder.doc1,
                                                 self.request)
        self.failUnless('advanced' not in
                        [a['extra']['id'] for a in actions])
        self.setRoles(('Manager',))
        actions = self.menu.getWorkflowMenuItems(self.folder.doc1,
                                                 self.request)
        self.failUnless('advanced' in
                        [a['extra']['id'] for a in actions])


class TestFactoriesMenu(PloneTestCase):

    layer = Layer

    def afterSetUp(self):
        self.folder.invokeFactory('Document', 'doc1')
        self.menu = getUtility(IBrowserMenu, name='ftw_contentmenu_factory',
                               context=self.folder)
        self.request = self.app.REQUEST

    def testMenuImplementsIBrowserMenu(self):
        self.failUnless(IBrowserMenu.providedBy(self.menu))

    def testMenuImplementsIFactoriesMenu(self):
        self.failUnless(IFactoriesMenu.providedBy(self.menu))

    def testMenuIncludesFactories(self):
        actions = self.menu.getMenuItems(self.folder, self.request)
        self.failUnless('image' in [a['extra']['id'] for a in actions])

    def test_menu_includes_factory_actions(self):
        folder_fti = self.portal.portal_types['Folder']
        folder_fti.addAction('test_factory_action',
                             'Test Factory Action',
                             'string:${object_url}', '', '',
                             'folder_factories')
        actions = self.menu.getMenuItems(self.folder, self.request)
        folder_fti = self.portal.portal_types['Folder']
        self.failUnless('test_factory_action' in [a['extra']['id']
                                                  for a in actions])
        # test with permissions
        folder_fti.addAction('test_factory_action_perm',
                             'Test Factory Action',
                             'string:${object_url}', '', 'Add portal content',
                             'folder_factories')
        actions = self.menu.getMenuItems(self.folder, self.request)
        folder_fti = self.portal.portal_types['Folder']
        self.failUnless('test_factory_action_perm' in [a['extra']['id']
                                                       for a in actions])

    def test_post_menu_item_adapter(self):
        actions = self.menu.getMenuItems(self.folder, self.request)
        # we should have some actions
        self.failUnless(len(actions) > 0)
        # register the null post factory menu adapter..
        provideAdapter(NullPostFactoryMenu,
                       (INullMarker, Interface),
                       IContentmenuPostFactoryMenu)
        alsoProvides(self.folder, INullMarker)
        adpt = queryMultiAdapter((self.folder, self.request),
                                 IContentmenuPostFactoryMenu)
        self.failUnless(isinstance(adpt, NullPostFactoryMenu))
        # .. then we should not have any more actions
        actions = self.menu.getMenuItems(self.folder, self.request)
        self.failUnless(len(actions) == 0)
        # and cleanup: lets remove the interface from the context
        noLongerProvides(self.folder, INullMarker)
        adpt = queryMultiAdapter((self.folder, self.request),
                                 IContentmenuPostFactoryMenu)
        self.failIf(isinstance(adpt, NullPostFactoryMenu))
