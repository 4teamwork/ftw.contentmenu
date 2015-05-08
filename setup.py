from setuptools import setup, find_packages
import os

version = '2.4.1.dev0'

tests_require = [
    'ftw.builder',
    'plone.app.testing',
    'unittest2',
    'zope.app.publisher',
    'zope.configuration',
    ]

setup(name='ftw.contentmenu',
      version=version,
      description="Customize Plone's content menu",
      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw contentmenu plone',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.contentmenu',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',

        # Zope
        'Acquisition',
        'zope.component',
        'zope.i18n',
        'zope.interface',

        # Plone
        'plone.app.contentmenu',
        'plone.app.upgrade',
        'Products.CMFCore',
        'Products.CMFPlone',

        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
