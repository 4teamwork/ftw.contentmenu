from zope.component import queryUtility, getUtility
from zope.app.publisher.interfaces.browser import IBrowserMenu
from plone.app.contentmenu.interfaces import IActionsMenu
from Products.PloneTestCase.ptc import PloneTestCase
from ftw.contentmenu.tests.layer import Layer


class TestActionsMenu(PloneTestCase):

    layer = Layer

    def afterSetUp(self):
        self.folder.invokeFactory('Document', 'doc1')
        self.menu = getUtility(IBrowserMenu, name='plone_contentmenu_actions', context=self.folder)
        self.request = self.app.REQUEST
        # add a 'object_buttons' action to the 'Folder' fti
        types_tool = self.portal.portal_types
        fti = types_tool['Folder']
        fti.addAction('tt_test', 'Test Action', 'string:${object_url}' ,'', '', 'object_buttons')

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
        actions = self.menu.getWorkflowMenuItems(self.folder.doc1, self.request)
        self.failUnless('workflow-transition-submit' in
                        [a['extra']['id'] for a in actions])
                        
    def test_workflowmenu_items_advanced(self):
        actions = self.menu.getWorkflowMenuItems(self.folder.doc1, self.request)
        self.failUnless('advanced' not in
                        [a['extra']['id'] for a in actions])
        self.setRoles(('Manager',))
        actions = self.menu.getWorkflowMenuItems(self.folder.doc1, self.request)
        self.failUnless('advanced' in
                        [a['extra']['id'] for a in actions])

