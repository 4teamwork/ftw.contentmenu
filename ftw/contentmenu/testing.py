from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from zope.configuration import xmlconfig


class FtwContentmenuLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ftw.contentmenu
        xmlconfig.file('configure.zcml', ftw.contentmenu,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.contentmenu:default')


FTW_CONTENTMENU_FIXTURE = FtwContentmenuLayer()
FTW_CONTENTMENU_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_CONTENTMENU_FIXTURE, ), name="FtwContentmenu:Integration")
