from plone.app.upgrade.utils import loadMigrationProfile


def to_v2001(context):
    """Updates profile.
    """
    loadMigrationProfile(context, 'profile-ftw.contentmenu.upgrades:to_v2001')
