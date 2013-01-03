.. contents::

Introduction
============

``ftw.contentmenu`` customizes Plone's content menu in the following way:

.. figure:: http://onegov.ch/approved.png/image
   :align: right
   :target: http://onegov.ch/community/zertifizierte-module/ftw.contentmenu

   Certified: 01/2013

* The workflow menu is removed. Workflow actions are displayed in 
  the actions menu instead.

* The Add... menu (aka folder factories) can additionally display actions
  having the category ``folder_factories``.

* The Add... menu can be customized further by providing a specific adapter
  which can modify the list of factory items.


Installation
============

Install ``ftw.contentmenu`` by adding it to the list of eggs in your buildout or by adding it as a dependency of your policy package. Then run buildout and
restart your instance.

::

  [instance]
  eggs =
      ftw.contenmenu

Go to Site Setup of your Plone site and activate the ``ftw.contentmenu``
add-on.

Links
=====

- Main github project repository: https://github.com/4teamwork/ftw.contentmenu
- Issue tracker: https://github.com/4teamwork/ftw.contentmenu/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.contentmenu
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.contentmenu


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.contentmenu`` is licensed under GNU General Public License, version 2.
