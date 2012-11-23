# pylint: disable=E0211, E0213
# E0211: Method has no argument
# E0213: Method should have "self" as first argument


from zope.interface import Interface


class IFtwContentmenuSpecific(Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IContentmenuPostFactoryMenu(Interface):
    """Interface for a adpater which is called after generating the list of
    factories for the current context. This adapter is called for cleaning
    up on custom content types. The default adapter does not change anything.

    Discriminants:
    - context
    - request
    """

    def __init__(context, request):
        """
        """

    def __call__(factories):
        """Clean up the factories and return a new list of factories. The
        factories are dicts with the infos for rendering the menu.
        See ftw.contentmenu.menu.FactoriesMenu
        """
