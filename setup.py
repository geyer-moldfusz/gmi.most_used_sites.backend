from setuptools import setup, find_packages
import sys, os

version = '0.1'

requires = [
    'cornice',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'webtest',
]

setup(name='gmi.mostusedsites.backend',
      version=version,
      description="REST backend for Most used Sites project",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Stefan Walluhn, Arne Winter',
      author_email='stefan@neuland.io',
      url='',
      license='GPLv3',
      packages=['gmi', 'gmi.mostusedsites', 'gmi.mostusedsites.backend'],
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      test_suite='gmi.mostusedsites.backend',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = gmi.mostusedsites.backend:main
      [console_scripts]
      initialize_db = gmi.mostusedsites.backend.scripts.initializedb:main
      """,
      )
