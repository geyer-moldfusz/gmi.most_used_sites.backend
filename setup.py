from setuptools import setup, find_packages
import sys, os

version = '0.1'

requires = [
    'colander',
    'cornice',
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
]

setup(name='gmi.mostusedsites.backend',
      version=version,
      description="REST backend for Most used sites project",
      long_description="""\
REST backend for Most used sites project
========================================

Collects browsing behavior gathered by the Most used sites Firefox Add-On. It
evaluates the data and presents them via a REST API.
""",
      classifiers=[
          'Framework :: Pyramid',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Topic :: Internet :: WWW/HTTP :: WSGI'
      ],
      keywords='geyer-moldfusz geyer moldfusz mostusedsites backend rest api',
      author='Stefan Walluhn, Arne Winter',
      author_email='stefan@neuland.io',
      url='https://github.com/geyer-moldfusz/gmi.most_used_sites.backend',
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
